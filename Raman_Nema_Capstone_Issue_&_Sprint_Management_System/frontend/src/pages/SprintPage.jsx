import { useEffect, useMemo, useState } from "react";
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
import { getRole } from "../utils/storage";
import "../styles/ProjectPage.css";

function SprintPage() {
  // Component state
  const [projects, setProjects] = useState([]);
  const [sprints, setSprints] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [selectedSprint, setSelectedSprint] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingSprints, setLoadingSprints] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

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
      loadSprints(selectedProjectId);
    }
  }, [selectedProjectId]);

  // Fetch all projects
  async function loadProjects() {
    setLoadingProjects(true);
    setError("");

    try {
      const response = await getProjects();
      const projectList = response.data.projects || [];

      setProjects(projectList);

      if (projectList.length > 0) {
        setSelectedProjectId((current) => current || projectList[0].id);
      }
    } catch (error) {
      setError(error.response?.data?.message || "Unable to load projects.");
    } finally {
      setLoadingProjects(false);
    }
  }

  // Fetch sprints for the selected project
  async function loadSprints(projectId) {
    setLoadingSprints(true);
    setError("");

    try {
      const response = await getProjectSprints(projectId);
      setSprints(response.data.sprints || []);
    } catch (error) {
      setSprints([]);
      setError(error.response?.data?.message || "Unable to load sprints.");
    } finally {
      setLoadingSprints(false);
    }
  }

  // Create a new sprint
  async function handleCreateSprint(sprintData) {
    if (!selectedProjectId) {
      setError("Select a project before creating a sprint.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      await createSprint(selectedProjectId, sprintData);
      await loadSprints(selectedProjectId);
      setSelectedSprint(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to create sprint.");
    } finally {
      setSaving(false);
    }
  }

  // Update an existing sprint
  async function handleUpdateSprint(sprintData) {
    setSaving(true);
    setError("");

    try {
      await updateSprint(selectedSprint.id, sprintData);
      await loadSprints(selectedProjectId);
      setSelectedSprint(null);
      setShowForm(false);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to update sprint.");
    } finally {
      setSaving(false);
    }
  }

  // Delete a sprint
  async function handleDeleteSprint(sprintId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this sprint?",
    );

    if (!confirmed) return;

    setError("");

    try {
      await deleteSprint(sprintId);
      await loadSprints(selectedProjectId);
    } catch (error) {
      setError(error.response?.data?.message || "Unable to delete sprint.");
    }
  }

  // Placeholder for viewing sprint issues
  function handleViewIssues(sprint) {
    window.alert(`Issues for ${sprint.name} will appear here soon.`);
  }

  // Handle project selection
  function handleProjectChange(event) {
    setSelectedProjectId(event.target.value);
    setSelectedSprint(null);
    setShowForm(false);
    setSearchTerm("");
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

  // Filter sprints by search text
  const filteredSprints = sprints.filter((sprint) =>
    sprint.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

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
              onDelete={handleDeleteSprint}
              onViewIssues={handleViewIssues}
            />
          ))}
      </div>
    </div>
  );
}

export default SprintPage;
