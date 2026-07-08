import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
  assignMember,
  removeMember,
} from "../services/project-service";
import ProjectForm from "../components/project/ProjectForm";
import ProjectCard from "../components/project/ProjectCard";
import Button from "../components/common/Button";
import ConfirmModal from "../components/common/ConfirmModal";
import Pagination from "../components/common/Pagination";
import { getRole } from "../utils/storage";
import {
  buildPaginationParams,
  DEFAULT_PAGE,
  getDefaultPagination,
} from "../utils/pagination";
import { useNotification } from "../context/useNotification";
import { ROUTES } from "../constants/navigation";
import "../styles/ProjectPage.css";

function ProjectPage() {
  const navigate = useNavigate();
  const { showNotification } = useNotification();
  // Component state
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [projectToDelete, setProjectToDelete] = useState(null);
  const [memberToRemove, setMemberToRemove] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(DEFAULT_PAGE);
  const [pagination, setPagination] = useState(getDefaultPagination());

  // Get current user role
  const role = getRole();
  const canEditProject = role === "ADMIN" || role === "MEMBER";

  // Load projects on page load
  useEffect(() => {
    loadProjects(page);
  }, [page]);

  // Fetch all projects
  async function loadProjects(nextPage = page) {
    setLoading(true);
    setError("");

    try {
      const response = await getProjects(buildPaginationParams(nextPage));
      setProjects(response.data.projects);
      setPagination(response.data.pagination || getDefaultPagination());
    } catch (error) {
      setError(error.response?.data?.message || "Unable to load projects.");
    } finally {
      setLoading(false);
    }
  }

  // Create a new project
  async function handleCreateProject(projectData) {
    setSaving(true);

    try {
      const response = await createProject(projectData);
      setPage(DEFAULT_PAGE);
      await loadProjects(DEFAULT_PAGE);
      setSelectedProject(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to create project.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  // Update an existing project
  async function handleUpdateProject(projectData) {
    setSaving(true);

    try {
      const response = await updateProject(selectedProject.id, projectData);
      await loadProjects();
      setSelectedProject(null);
      setShowForm(false);
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to update project.";
      setError(message);
      showNotification(message, "error");
    } finally {
      setSaving(false);
    }
  }

  // Delete a project
  async function confirmDeleteProject() {
    if (!projectToDelete) return;
    try {
      const response = await deleteProject(projectToDelete);
      await loadProjects();
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to delete project.";
      showNotification(message, "error");
    } finally {
      setProjectToDelete(null);
    }
  }

  // Assign a member to a project
  async function handleAssignMember(projectId, userId) {
    setError("");

    if (!/^[a-f\d]{24}$/i.test(userId)) {
      const message = "Enter a valid member user ID.";
      setError(message);
      showNotification(message, "error");
      return;
    }

    try {
      const response = await assignMember(projectId, userId);
      await loadProjects();
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to assign member.";
      setError(message);
      showNotification(message, "error");
    }
  }

  // Remove a project member
  async function confirmRemoveMember() {
    if (!memberToRemove) return;
    setError("");

    try {
      const response = await removeMember(
        memberToRemove.projectId,
        memberToRemove.userId,
      );
      await loadProjects();
      showNotification(response.message);
    } catch (error) {
      const message =
        error.response?.data?.message || "Unable to remove member.";
      showNotification(message, "error");
    } finally {
      setMemberToRemove(null);
    }
  }

  // Filter projects by search text
  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="project-page">
      <div className="project-container">
        <h1>Projects</h1>

        {/* Search and create toolbar */}
        <div className="form-group">
          <label className="toolbar-label">Search Project</label>

          <div className="toolbar">
            <input
              className="search-input"
              name="search"
              type="text"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
            />

            {/* Only ADMIN can create projects */}
            {role === "ADMIN" && (
              <Button
                text="Create Project"
                className="btn-success"
                onClick={() => {
                  setSelectedProject(null);
                  setShowForm(true);
                }}
              />
            )}
          </div>
        </div>

        {/* Project form */}
        {canEditProject && showForm && (
          <ProjectForm
            key={selectedProject?.id || "new-project"}
            initialData={selectedProject}
            onSubmit={
              selectedProject ? handleUpdateProject : handleCreateProject
            }
            onCancel={() => {
              setSelectedProject(null);
              setShowForm(false);
            }}
            loading={saving}
          />
        )}

        {/* Page states */}
        {loading && <p>Loading projects...</p>}
        {error && <p className="error-message">{error}</p>}

        {!loading && !error && filteredProjects.length === 0 && (
          <p>No projects found.</p>
        )}

        {/* Project list */}
        {!loading &&
          !error &&
          filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onEdit={(project) => {
                setSelectedProject(project);
                setShowForm(true);
              }}
              onDelete={setProjectToDelete}
              onViewSprints={(projectId) => {
                navigate(`${ROUTES.SPRINTS}?projectId=${projectId}`);
              }}
              onAssignMember={handleAssignMember}
              onRemoveMember={(projectId, userId) => {
                setMemberToRemove({ projectId, userId });
              }}
            />
          ))}

        {!loading && !error && (
          <Pagination
            pagination={pagination}
            disabled={loading}
            onPageChange={setPage}
          />
        )}

        {memberToRemove && (
          <ConfirmModal
            title="Remove member"
            message="Are you sure you want to remove this member from the project?"
            confirmText="Remove"
            onCancel={() => setMemberToRemove(null)}
            onConfirm={confirmRemoveMember}
          />
        )}

        {projectToDelete && (
          <ConfirmModal
            title="Delete project"
            message="Are you sure you want to delete this project?"
            confirmText="Delete"
            onCancel={() => setProjectToDelete(null)}
            onConfirm={confirmDeleteProject}
          />
        )}
      </div>
    </div>
  );
}

export default ProjectPage;
