import { useEffect, useState } from "react";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
} from "../services/project-service";
import ProjectForm from "../components/project/ProjectForm";
import ProjectCard from "../components/project/ProjectCard";
import Button from "../components/common/Button";
import { getRole } from "../utils/storage";
import "../styles/ProjectPage.css";

function ProjectPage() {
  // Store all projects returned by the backend.
  const [projects, setProjects] = useState([]);

  // Track whether data is currently being loaded.
  const [loading, setLoading] = useState(true);

  // Store API error messages.
  const [error, setError] = useState("");

  // Control the visibility of the project form.
  const [showForm, setShowForm] = useState(false);

  // Track whether a create or update request is in progress.
  const [saving, setSaving] = useState(false);

  // Store the project currently being edited.
  const [selectedProject, setSelectedProject] = useState(null);

  // Store the search text.
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    setLoading(true);
    setError("");

    try {
      // Fetch all projects.
      const response = await getProjects();

      setProjects(response.data.projects);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to load projects.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateProject(projectData) {
    setSaving(true);

    try {
      // Create a project.
      await createProject(projectData);

      // Refresh the project list.
      await loadProjects();

      // Close the form.
      setSelectedProject(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to create project.");
    } finally {
      setSaving(false);
    }
  }

  async function handleUpdateProject(projectData) {
    setSaving(true);

    try {
      // Update the selected project.
      await updateProject(selectedProject.id, projectData);

      // Refresh the project list.
      await loadProjects();

      // Exit edit mode.
      setSelectedProject(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to update project.");
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteProject(projectId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this project?",
    );

    if (!confirmed) {
      return;
    }

    try {
      // Delete the project.
      await deleteProject(projectId);

      // Refresh the project list.
      await loadProjects();
    } catch (error) {
      setError(error.response?.data?.message || "Unable to delete project.");
    }
  }

  // Filter projects by project name.
  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="project-page">
      <div className="project-container">
        <h1>Projects</h1>

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

            {getRole() !== "VIEWER" && (
              <Button
                text="Create Project"
                onClick={() => {
                  setSelectedProject(null);
                  setShowForm(true);
                }}
              />
            )}
          </div>
        </div>

        {getRole() !== "VIEWER" && showForm && (
          <ProjectForm
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

        {loading && <p>Loading projects...</p>}

        {error && <p className="error-message">{error}</p>}

        {!loading && !error && filteredProjects.length === 0 && (
          <p>No projects found.</p>
        )}
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
            />
          ))}
      </div>
    </div>
  );
}

export default ProjectPage;