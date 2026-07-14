import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getProjects } from "../services/project-service";
import {
  createSprint,
  deleteSprint,
  getProjectSprints,
  updateSprint,
} from "../services/sprint-service";
import SprintForm from "../components/sprint/SprintForm";
import SprintCard from "../components/sprint/SprintCard";
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

function SprintPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { showNotification } = useNotification();
  // Component state
  const [projects, setProjects] = useState([]);
  const [sprints, setSprints] = useState([]);
  const [sprintOptions, setSprintOptions] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(
    searchParams.get("projectId") || "",
  );
  const [selectedSprintId, setSelectedSprintId] = useState(
    searchParams.get("sprintId") || "",
  );
  const [selectedSprint, setSelectedSprint] = useState(null);
  const [sprintToDelete, setSprintToDelete] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingSprints, setLoadingSprints] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(DEFAULT_PAGE);
  const [pagination, setPagination] = useState(getDefaultPagination());

  // Get current user role
  const role = getRole();
  const canManageSprints = role === "ADMIN" || role === "MEMBER";

  // Load projects on page load
  useEffect(() => {
    loadProjects();
  }, []);

  // Load sprints when project changes
  useEffect(() => {
    if (selectedProjectId) {
      loadSprints(selectedProjectId, page);
      loadSprintOptions(selectedProjectId);
    }
  }, [selectedProjectId, page]);

  useEffect(() => {
    if (selectedProjectId) {
      setSearchParams((previous) => {
        const params = new URLSearchParams(previous);
        params.set("projectId", selectedProjectId);
        params.set("page", String(page));

        if (selectedSprintId) {
          params.set("sprintId", selectedSprintId);
        } else {
          params.delete("sprintId");
        }

        return params;
      });
    }
  }, [selectedProjectId, page, selectedSprintId]);

  // Fetch all projects
  async function loadProjects() {
    setLoadingProjects(true);
    setError("");

    try {
      const response = await getProjects({ limit: 100 });
      const projectList = response.data.projects || [];
      const requestedProjectId = searchParams.get("projectId");
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

  // Fetch sprints for the selected project
  async function loadSprints(projectId, nextPage = page) {
    setLoadingSprints(true);
    setError("");

    try {
      const response = await getProjectSprints(
        projectId,
        buildPaginationParams(nextPage),
      );
      setSprints(response.data.sprints || []);
      setPagination(response.data.pagination || getDefaultPagination());
    } catch (error) {
      setSprints([]);
      setPagination(getDefaultPagination());
      setError(error.response?.data?.message || "Unable to load sprints.");
    } finally {
      setLoadingSprints(false);
    }
  }

  async function loadSprintOptions(projectId) {
    try {
      const response = await getProjectSprints(projectId, { limit: 100 });
      const sprintList = response.data.sprints || [];
      const requestedSprintId = searchParams.get("sprintId");

      setSprintOptions(sprintList);

      setSelectedSprintId((current) => {
        const preferredSprintId = current || requestedSprintId;
        const hasPreferredSprint = sprintList.some(
          (sprint) => sprint.id === preferredSprintId,
        );

        return hasPreferredSprint ? preferredSprintId : "";
      });
    } catch {
      setSprintOptions([]);
      setSelectedSprintId("");
    }
  }

  // Create a new sprint
  async function handleCreateSprint(sprintData) {
    if (!selectedProjectId) {
      const message = "Select a project before creating a sprint.";
      setError(message);
      showNotification(message, "error");
      return;
    }

    setSaving(true);
    setError("");

    try {
      const response = await createSprint(selectedProjectId, sprintData);
      setPage(DEFAULT_PAGE);
      await loadSprints(selectedProjectId, DEFAULT_PAGE);
      setSelectedSprint(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to create sprint.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  // Update an existing sprint
  async function handleUpdateSprint(sprintData) {
    setSaving(true);
    setError("");

    try {
      const response = await updateSprint(selectedSprint.id, sprintData);
      await loadSprints(selectedProjectId);
      setSelectedSprint(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to update sprint.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  // Delete a sprint
  async function confirmDeleteSprint() {
    if (!sprintToDelete) return;
    setError("");

    try {
      const response = await deleteSprint(sprintToDelete);
      await loadSprints(selectedProjectId);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to delete sprint.";
      showNotification(message, "error");
    } finally {
      setSprintToDelete(null);
    }
  }

  function handleViewIssues(sprint) {
    navigate(`/issues?projectId=${sprint.project_id}&sprintId=${sprint.id}`);
  }

  // Handle project selection
  function handleProjectChange(event) {
    setSelectedProjectId(event.target.value);
    setSelectedSprintId("");
    setPage(DEFAULT_PAGE);
    setSelectedSprint(null);
    setShowForm(false);
    setSearchTerm("");
  }

  function handleSprintFilterChange(event) {
    setSelectedSprintId(event.target.value);
    setPage(DEFAULT_PAGE);
    setSelectedSprint(null);
    setShowForm(false);
  }

  // Get selected project
  const selectedProject = projects.find(
    (project) => project.id === selectedProjectId,
  );

  // Map project IDs to names
  const projectNameById = useMemo(() => {
    return projects.reduce((names, project) => {
      names[project.id] = project.name;
      return names;
    }, {});
  }, [projects]);

  // Filter sprints by selected sprint and search text
  const sprintList = selectedSprintId ? sprintOptions : sprints;
  const filteredSprints = sprintList.filter((sprint) => {
    const matchesSprint = selectedSprintId
      ? sprint.id === selectedSprintId
      : true;
    const matchesSearch = sprint.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    return matchesSprint && matchesSearch;
  });

  return (
    <div className="project-page">
      <div className="project-container">
        <h1>Sprints</h1>

        {/* Project selector and search */}
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
              onChange={handleSprintFilterChange}
              disabled={!selectedProjectId || loadingSprints}
            >
              <option value="">All sprints</option>

              {sprintOptions.map((sprint) => (
                <option key={sprint.id} value={sprint.id}>
                  {sprint.name}
                </option>
              ))}
            </select>

            <input
              className="search-input"
              name="search"
              type="text"
              placeholder="Search sprint"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              disabled={!selectedProjectId}
            />

            {canManageSprints && (
              <Button
                text="Create Sprint"
                className="btn-success"
                disabled={!selectedProjectId}
                onClick={() => {
                  setSelectedSprint(null);
                  setShowForm(true);
                }}
              />
            )}
          </div>
        </div>

        {/* Sprint form */}
        {canManageSprints && showForm && (
          <SprintForm
            key={selectedSprint?.id || "new-sprint"}
            initialData={selectedSprint}
            onSubmit={selectedSprint ? handleUpdateSprint : handleCreateSprint}
            onCancel={() => {
              setSelectedSprint(null);
              setShowForm(false);
            }}
            loading={saving}
          />
        )}

        {/* Page states */}
        {loadingProjects && <p>Loading projects...</p>}
        {!loadingProjects && loadingSprints && <p>Loading sprints...</p>}
        {error && <p className="error-message">{error}</p>}

        {!loadingProjects && !error && projects.length === 0 && (
          <p>No projects found.</p>
        )}

        {!loadingProjects &&
          !loadingSprints &&
          !error &&
          selectedProjectId &&
          filteredSprints.length === 0 && <p>No sprints found.</p>}

        {/* Sprint list */}
        {!loadingProjects &&
          !loadingSprints &&
          !error &&
          filteredSprints.map((sprint) => (
            <SprintCard
              key={sprint.id}
              sprint={sprint}
              projectName={
                projectNameById[sprint.project_id] || selectedProject?.name
              }
              onEdit={(sprint) => {
                setSelectedSprint(sprint);
                setShowForm(true);
              }}
              onDelete={setSprintToDelete}
              onViewIssues={handleViewIssues}
            />
          ))}

        {!loadingProjects && !loadingSprints && !error && (
          <Pagination
            pagination={pagination}
            disabled={loadingSprints}
            onPageChange={setPage}
          />
        )}

        {sprintToDelete && (
          <ConfirmModal
            title="Delete sprint"
            message="Are you sure you want to delete this sprint?"
            confirmText="Delete"
            onCancel={() => setSprintToDelete(null)}
            onConfirm={confirmDeleteSprint}
          />
        )}
      </div>
    </div>
  );
}

export default SprintPage;
