import React, { useState } from 'react';
import DocumentComponent from './Documents';
import AddProjectModal from './component/AddProjectModal';
import AddDocumentModal from './component/AddDocumentModal';
import './style/style.css';

export default function ProjectComponent({ projects, onAddProject, onAddDocument, onDeleteDocument }) {
  
  const [expandedProjectId, setExpandedProjectId] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showAddDocumentModal, setShowAddDocumentModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);

  const toggleProject = (projectId) => {
    setExpandedProjectId((prev) =>
      prev === projectId ? null : projectId
    );
  };

  const handleAddProject = async (projectData) => {
    await onAddProject(projectData);
    setShowAddModal(false);
  };

  const onEditProject = (project) => {
    console.log('Modifier le projet', project);
  };

  const onDeleteProject = (project) => {
    const confirmed = window.confirm(
      `Supprimer le projet "${project.name}" ?`
    );

    if (!confirmed) return;

    console.log('Supprimer le projet', project);
  };

  const handleAddDocumentClick = (project) => {
    setSelectedProject(project);
    setShowAddDocumentModal(true);
  };

  const handleAddDocument = async (file) => {
    if (selectedProject) {
      await onAddDocument(selectedProject.id, file);
      setShowAddDocumentModal(false);
      setSelectedProject(null);
    }
  };

  const onViewDocument = (project, document) => {
    console.log('Voir le document', project, document);
  };

  const onEditDocument = (project, document) => {
    console.log('Modifier le document', project, document);
  };

  const handleDeleteDocument = async (doc) => {
    const confirmed = window.confirm(
      `Supprimer le document "${doc.filename}" ?`
    );

    if (!confirmed) return;

    try {
      await onDeleteDocument(doc.id);
    } catch (err) {
      console.error('Error deleting document:', err);
      alert('Erreur lors de la suppression du document');
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="projects-title">Projets</h2>

        <button
          type="button"
          className="btn btn-sm text-white"
          style={{
            backgroundColor: '#0B1849',
            borderColor: '#0B1849',
          }}
          onClick={() => setShowAddModal(true)}
        >
          <i className="bi bi-plus-lg me-1"></i>
          Ajouter un projet
        </button>
      </div>

      <table className="table projects-table align-middle mb-0">
        <thead>
          <tr>
            <th style={{ width: 36 }}></th>
            <th>PROJECT</th>
            <th>RESPONSABLE</th>
            <th>DOCUMENTS</th>
            <th style={{ width: 110 }}>ACTIONS</th>
          </tr>
        </thead>

        <tbody>
          {projects.map((project) => {
            const isOpen = expandedProjectId === project.id;

            return (
              <React.Fragment key={project.id}>
                <tr
                  className="project-row"
                  onClick={() => toggleProject(project.id)}
                >
                  <td>
                    <i
                      className={`bi bi-chevron-right chevron-icon ${
                        isOpen ? 'open' : ''
                      }`}
                    ></i>
                  </td>

                  <td className="project-name">
                    <div className="d-flex align-items-center">
                      <div className="project-icon-wrapper me-3">
                        <i className="bi bi-folder"></i>
                      </div>
                      <div>
                        <div className="fw-semibold">{project.name}</div>
                        <small className="text-muted">Last updated 2 days ago</small>
                      </div>
                    </div>
                  </td>

                  <td className="project-responsable">
                    <span>Ahmed</span>
                  </td>

                  <td>
                    <span className="documents-badge">
                      {project.documents?.length || 0} Documents
                    </span>
                  </td>

                  <td>
                    <div
                      className="action-icons"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <i
                        className="bi bi-pencil action-edit"
                        title="Modifier"
                        onClick={() => onEditProject(project)}
                      ></i>

                      <i
                        className="bi bi-trash action-delete"
                        title="Supprimer"
                        onClick={() => onDeleteProject(project)}
                      ></i>
                    </div>
                  </td>
                </tr>

                {isOpen && (
                  <tr className="project-details-row show">
                    <td colSpan={5}>
                      <div className="documents-wrapper">
                        <DocumentComponent
                          documents={project.documents || []}
                          pageSize={8}
                          onAdd={() => handleAddDocumentClick(project)}
                          onView={(document) =>
                            onViewDocument(project, document)
                          }
                          onEdit={(document) =>
                            onEditDocument(project, document)
                          }
                          onDelete={(document) =>
                            handleDeleteDocument(document)
                          }
                        />
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>

      <AddProjectModal
        visible={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSubmit={handleAddProject}
      />

      <AddDocumentModal
        visible={showAddDocumentModal}
        onClose={() => {
          setShowAddDocumentModal(false);
          setSelectedProject(null);
        }}
        onSubmit={handleAddDocument}
        projectName={selectedProject?.name}
      />
    </div>
  );
}