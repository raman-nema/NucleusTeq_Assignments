import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getProjects } from "../services/project-service";
import { getProjectSprints } from "../services/sprint-service";
import {
  addIssueComment,
  createIssue,
  deleteIssue,
  deleteIssueComment,
  getProjectIssues,
  updateIssue,
} from "../services/issue-service";
import IssueForm from "../components/issue/IssueForm";
import IssueCard from "../components/issue/IssueCard";
import Button from "../components/common/Button";
import ConfirmModal from "../components/common/ConfirmModal";
import Pagination from "../components/common/Pagination";
import { getRole } from "../utils/storage";
import { useNotification } from "../context/useNotification";
import {
  buildPaginationParams,
  DEFAULT_PAGE,
  getDefaultPagination,
} from "../utils/pagination";
import "../styles/project-styles";

function IssuePage() {
  const { showNotification } = useNotification();
  const [searchParams, setSearchParams] = useSearchParams();
  const [projects, setProjects] = useState([]);
  const [sprints, setSprints] = useState([]);
  const [issues, setIssues] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(
    searchParams.get("projectId") || "",
  );
  const [selectedSprintId, setSelectedSprintId] = useState(
    searchParams.get("sprintId") || "",
  );
  const [statusFilter, setStatusFilter] = useState(
    searchParams.get("status") || "",
  );
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [issueToDelete, setIssueToDelete] = useState(null);
  const [commentToDelete, setCommentToDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingSprints, setLoadingSprints] = useState(false);
  const [loadingIssues, setLoadingIssues] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(DEFAULT_PAGE);
  const [pagination, setPagination] = useState(getDefaultPagination());

  const role = getRole();
  const canManageIssues = role === "ADMIN" || role === "MEMBER";
  const requestedProjectId = searchParams.get("projectId");
  const requestedSprintId = searchParams.get("sprintId");

  useEffect(() => {
    loadProjects();
  }, []);

  useEffect(() => {
    if (selectedProjectId) {
      loadSprints(selectedProjectId);
      loadIssues(selectedProjectId, page, statusFilter);
      setSearchParams((previous) => {
        const params = new URLSearchParams(previous);
        params.set("projectId", selectedProjectId);
        params.set("page", String(page));

        if (statusFilter) {
          params.set("status", statusFilter);
        } else {
          params.delete("status");
        }

        return params;
      });
    }
  }, [selectedProjectId, page, statusFilter]);

  useEffect(() => {
    setSearchParams((previous) => {
      const params = new URLSearchParams(previous);

      if (selectedSprintId) {
        params.set("sprintId", selectedSprintId);
      } else {
        params.delete("sprintId");
      }

      return params;
    });
  }, [selectedSprintId]);

  async function loadProjects() {
    setLoadingProjects(true);
    setError("");

    try {
      const response = await getProjects({ limit: 100 });
      const projectList = response.data.projects || [];
      const hasRequestedProject = projectList.some(
        (project) => project.id === requestedProjectId,
      );

      setProjects(projectList);

      if (projectList.length > 0) {
        setSelectedProjectId((current) => {
          if (current && projectList.some((project) => project.id === current)) {
            return current;
          }

          return hasRequestedProject ? requestedProjectId : projectList[0].id;
        });
      }
    } catch (error) {
      setError(error.response?.data?.message || "Unable to load projects.");
    } finally {
      setLoadingProjects(false);
    }
  }

  async function loadSprints(projectId) {
    setLoadingSprints(true);
    setError("");

    try {
      const response = await getProjectSprints(projectId, { limit: 100 });
      const sprintList = response.data.sprints || [];

      setSprints(sprintList);

      setSelectedSprintId((current) => {
        const preferredSprintId = current || requestedSprintId;
        const hasPreferredSprint = sprintList.some(
          (sprint) => sprint.id === preferredSprintId,
        );

        return hasPreferredSprint ? preferredSprintId : "";
      });
    } catch (error) {
      setSprints([]);
      setSelectedSprintId("");
      setError(error.response?.data?.message || "Unable to load sprints.");
    } finally {
      setLoadingSprints(false);
    }
  }

  async function loadIssues(
    projectId,
    nextPage = page,
    nextStatus = statusFilter,
  ) {
    setLoadingIssues(true);
    setError("");

    try {
      const response = await getProjectIssues(
        projectId,
        {
          ...buildPaginationParams(nextPage),
          ...(nextStatus ? { status: nextStatus } : {}),
        },
      );
      setIssues(response.data.issues || []);
      setPagination(response.data.pagination || getDefaultPagination());
    } catch (error) {
      setIssues([]);
      setPagination(getDefaultPagination());
      setError(error.response?.data?.message || "Unable to load issues.");
    } finally {
      setLoadingIssues(false);
    }
  }

  async function handleCreateIssue(issueData) {
    if (!selectedProjectId) {
      const message = "Select a project before creating an issue.";
      setError(message);
      showNotification(message, "error");
      return;
    }

    setSaving(true);
    setError("");

    try {
      const response = await createIssue(selectedProjectId, issueData);
      setPage(DEFAULT_PAGE);
      await loadIssues(selectedProjectId, DEFAULT_PAGE, statusFilter);
      setSelectedIssue(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to create issue.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  async function handleUpdateIssue(issueData) {
    setSaving(true);
    setError("");

    try {
      const response = await updateIssue(selectedIssue.id, issueData);
      await loadIssues(selectedProjectId, page, statusFilter);
      setSelectedIssue(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to update issue.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  async function handleAddComment(issueId, text) {
    setError("");

    try {
      const response = await addIssueComment(issueId, { text });
      const updatedIssue = response.data;

      setIssues((currentIssues) =>
        currentIssues.map((issue) =>
          issue.id === issueId
            ? {
                ...issue,
                ...updatedIssue,
                comments: updatedIssue.comments || [],
              }
            : issue,
        ),
      );

      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to add comment.";
      setError(message);
      showNotification(message, "error");
      throw error;
    }
  }

  async function confirmDeleteComment() {
    if (!commentToDelete) return;
    setError("");

    try {
      const response = await deleteIssueComment(
        commentToDelete.issueId,
        commentToDelete.commentId,
      );
      const updatedIssue = response.data;

      setIssues((currentIssues) =>
        currentIssues.map((issue) =>
          issue.id === commentToDelete.issueId
            ? {
                ...issue,
                ...updatedIssue,
                comments: updatedIssue.comments || [],
              }
            : issue,
        ),
      );

      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to delete comment.";
      showNotification(message, "error");
    } finally {
      setCommentToDelete(null);
    }
  }

  async function confirmDeleteIssue() {
    if (!issueToDelete) return;
    setError("");

    try {
      const response = await deleteIssue(issueToDelete);
      await loadIssues(selectedProjectId, page, statusFilter);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to delete issue.";
      showNotification(message, "error");
    } finally {
      setIssueToDelete(null);
    }
  }

  function handleProjectChange(event) {
    setSelectedProjectId(event.target.value);
    setSelectedSprintId("");
    setPage(DEFAULT_PAGE);
    setSelectedIssue(null);
    setShowForm(false);
    setSearchTerm("");
  }

  function handleStatusFilterChange(event) {
    setStatusFilter(event.target.value);
    setPage(DEFAULT_PAGE);
    setSelectedIssue(null);
    setShowForm(false);
  }

  function handleSprintChange(event) {
    setSelectedSprintId(event.target.value);
    setPage(DEFAULT_PAGE);
    setSelectedIssue(null);
    setShowForm(false);
  }

  const selectedProject = projects.find(
    (project) => project.id === selectedProjectId,
  );

  const members = useMemo(() => selectedProject?.members || [], [
    selectedProject,
  ]);

  const assignableMembers = useMemo(() => {
    return members.filter((member) => member.role === "MEMBER");
  }, [members]);

  const sprintNameById = useMemo(() => {
    return sprints.reduce((names, sprint) => {
      names[sprint.id] = sprint.name;
      return names;
    }, {});
  }, [sprints]);

  const memberNameById = useMemo(() => {
    return members.reduce((names, member) => {
      names[member.id] = member.name;
      return names;
    }, {});
  }, [members]);

  const filteredIssues = issues.filter((issue) => {
    const matchesSprint = selectedSprintId
      ? issue.sprint_id === selectedSprintId
      : true;
    const term = searchTerm.toLowerCase();
    const matchesSearch =
      issue.title.toLowerCase().includes(term) ||
      issue.description.toLowerCase().includes(term);

    return matchesSprint && matchesSearch;
  });

  return (
    <div className="project-page">
      <div className="project-container">
        <h1>Issues</h1>

        <div className="form-group">
          <label className="toolbar-label">Project</label>

          <div className="toolbar sprint-toolbar">
            <select
              className="search-input select-input"
              value={selectedProjectId}
              onChange={handleProjectChange}
              disabled={loadingProjects || projects.length === 0}
            >
              {projects.length === 0 && <option value="">No projects</option>}

              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>

            <select
              className="search-input select-input"
              value={selectedSprintId}
              onChange={handleSprintChange}
              disabled={!selectedProjectId || loadingSprints}
            >
              <option value="">All sprints</option>

              {sprints.map((sprint) => (
                <option key={sprint.id} value={sprint.id}>
                  {sprint.name}
                </option>
              ))}
            </select>

            <select
              className="search-input select-input"
              value={statusFilter}
              onChange={handleStatusFilterChange}
              disabled={!selectedProjectId}
            >
              <option value="">All statuses</option>
              <option value="TODO">Todo</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="DONE">Done</option>
            </select>

            <input
              className="search-input"
              name="search"
              type="text"
              placeholder="Search issue"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              disabled={!selectedProjectId}
            />

            {canManageIssues && (
              <Button
                text="Create Issue"
                className="btn-success"
                disabled={
                  !selectedProjectId ||
                  sprints.length === 0 ||
                  assignableMembers.length === 0
                }
                onClick={() => {
                  setSelectedIssue(null);
                  setShowForm(true);
                }}
              />
            )}
          </div>
        </div>

        {canManageIssues && showForm && (
          <IssueForm
            key={selectedIssue?.id || selectedSprintId || "new-issue"}
            initialData={selectedIssue}
            sprints={sprints}
            members={assignableMembers}
            selectedSprintId={selectedIssue?.sprint_id || selectedSprintId}
            onSubmit={selectedIssue ? handleUpdateIssue : handleCreateIssue}
            onCancel={() => {
              setSelectedIssue(null);
              setShowForm(false);
            }}
            loading={saving}
          />
        )}

        {loadingProjects && <p>Loading projects...</p>}
        {!loadingProjects && loadingSprints && <p>Loading sprints...</p>}
        {!loadingProjects && loadingIssues && <p>Loading issues...</p>}
        {error && <p className="error-message">{error}</p>}

        {!loadingProjects && !error && projects.length === 0 && (
          <p>No projects found.</p>
        )}

        {!loadingProjects &&
          !loadingSprints &&
          !loadingIssues &&
          !error &&
          selectedProjectId &&
          sprints.length === 0 && <p>No sprints found for this project.</p>}

        {!loadingProjects &&
          !loadingSprints &&
          !loadingIssues &&
          !error &&
          selectedProjectId &&
          sprints.length > 0 &&
          filteredIssues.length === 0 && <p>No issues found.</p>}

        {!loadingProjects &&
          !loadingSprints &&
          !loadingIssues &&
          !error &&
          filteredIssues.map((issue) => (
            <IssueCard
              key={issue.id}
              issue={issue}
              sprintName={sprintNameById[issue.sprint_id]}
              assigneeName={memberNameById[issue.assignee]}
              reporterName={memberNameById[issue.reporter]}
              onEdit={(issue) => {
                setSelectedIssue(issue);
                setShowForm(true);
              }}
              onDelete={setIssueToDelete}
              onAddComment={handleAddComment}
              onDeleteComment={(issueId, commentId) => {
                setCommentToDelete({ issueId, commentId });
              }}
            />
          ))}

        {!loadingProjects && !loadingSprints && !loadingIssues && !error && (
          <Pagination
            pagination={pagination}
            disabled={loadingIssues}
            onPageChange={setPage}
          />
        )}

        {issueToDelete && (
          <ConfirmModal
            title="Delete issue"
            message="Are you sure you want to delete this issue?"
            confirmText="Delete"
            onCancel={() => setIssueToDelete(null)}
            onConfirm={confirmDeleteIssue}
          />
        )}

        {commentToDelete && (
          <ConfirmModal
            title="Delete comment"
            message="Are you sure you want to delete this comment?"
            confirmText="Delete"
            onCancel={() => setCommentToDelete(null)}
            onConfirm={confirmDeleteComment}
          />
        )}
      </div>
    </div>
  );
}

export default IssuePage;
