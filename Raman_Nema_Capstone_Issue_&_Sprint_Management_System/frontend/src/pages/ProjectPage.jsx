import { useEffect, useState } from "react";
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
import { getRole } from "../utils/storage";
import "../styles/ProjectPage.css";

function ProjectPage() {
  // Component state
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  // Get current user role
  const role = getRole();
  const canEditProject = role === "ADMIN" || role === "MEMBER";

  // Load projects on page load
  useEffect(() => {
    loadProjects();
  }, []);

  // Fetch all projects
  async function loadProjects() {
    setLoading(true);
    setError("");

    try {
      const response = await getProjects();
      setProjects(response.data.projects);
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
      await createProject(projectData);
      await loadProjects();
      setSelectedProject(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to create project.");
    } finally {
      setSaving(false);
    }
  }

  // Update an existing project
  async function handleUpdateProject(projectData) {
    setSaving(true);

    try {
      await updateProject(selectedProject.id, projectData);
      await loadProjects();
      setSelectedProject(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to update project.");
    } finally {
      setSaving(false);
    }
  }

  // Delete a project
  async function handleDeleteProject(projectId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this project?",
    );

    if (!confirmed) return;

    try {
      await deleteProject(projectId);
      await loadProjects();
    } catch (error) {
      setError(error.response?.data?.message || "Unable to delete project.");
    }
  }

  // Assign a member to a project
  async function handleAssignMember(projectId, userId) {
    setError("");

    if (!/^[a-f\d]{24}$/i.test(userId)) {
      setError("Enter a valid member user ID.");
      return;
    }

    try {
      await assignMember(projectId, userId);
      await loadProjects();
    } catch (error) {
      setError(error.response?.data?.message || "Unable to assign member.");
    }
  }

  // Remove a project member
  async function handleRemoveMember(projectId, userId) {
    const confirmed = window.confirm(
      "Are you sure you want to remove this member from the project?",
    );

    if (!confirmed) return;

    setError("");

    try {
      await removeMember(projectId, userId);
      await loadProjects();
    } catch (error) {
      setError(error.response?.data?.message || "Unable to remove member.");
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
              onDelete={handleDeleteProject}
              onAssignMember={handleAssignMember}
              onRemoveMember={handleRemoveMember}
            />
          ))}
      </div>
    </div>
  );
}

export default ProjectPage;