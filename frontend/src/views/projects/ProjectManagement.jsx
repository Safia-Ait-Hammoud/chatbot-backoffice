import React, { useEffect, useState } from 'react'
import ProjectComponent from './Projects'

import {
  getDocumentsByProjectId,
  addDocument,
  delete_document,
} from '../../shared/services/document.service'

import {
  getAllProjects,
  addProject,
} from '../../shared/services/project.service'

export default function ProjectManagement() {
  const [projects, setProjects] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const projects = await getAllProjects();
      console.log('Loaded projects:', projects)
      console.log('Projects is array?', Array.isArray(projects))

      if (!Array.isArray(projects)) {
        console.error('Projects is not an array:', projects)
        setError(new Error('Invalid projects data received'))
        return
      }

      const projectsWithDocuments = await Promise.all(
        projects.map(async (project) => {
          const documents = await getDocumentsByProjectId(project.id);

          return {
            ...project,
            documents: Array.isArray(documents) ? documents : [],
          };
        })
      );

      setProjects(projectsWithDocuments);
    } catch (err) {
      console.error('Error loading projects:', err);
      setError(err);
    }
  };

  const handleAddProject = async (projectData) => {
    try {
      const newProject = await addProject(projectData);
      console.log('Project added:', newProject);
      //reload
      await loadProjects();
    } catch (err) {
      console.error('Error adding project:', err);
      throw err;
    }
  };

  const handleAddDocument = async (projectId, file) => {
    try {
      const newDocument = await addDocument(projectId, file);
      console.log('Document added:', newDocument);
      
      // Reload projects after adding document
      await loadProjects();
    } catch (err) {
      console.error('Error adding document:', err);
      throw err;
    }
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await delete_document(documentId);
      console.log('Document deleted:', documentId);
      
      // Reload projects after deleting document
      await loadProjects();
    } catch (err) {
      console.error('Error deleting document:', err);
      throw err;
    }
  };

  return (
    <div>
      <ProjectComponent 
        projects={projects} 
        onAddProject={handleAddProject}
        onAddDocument={handleAddDocument}
        onDeleteDocument={handleDeleteDocument}
      />
    </div>
  );
}