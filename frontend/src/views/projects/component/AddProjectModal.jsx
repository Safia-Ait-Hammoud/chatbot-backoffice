import React, { useState } from 'react';
import {
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CButton,
  CForm,
  CFormLabel,
  CFormInput,
} from '@coreui/react';

export default function AddProjectModal({ visible, onClose, onSubmit }) {
  const [projectName, setProjectName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!projectName.trim()) {
      setError('Le nom du projet est requis');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      await onSubmit({ name: projectName.trim() });
      // Reset form on success
      setProjectName('');
      onClose();
    } catch (err) {
      setError(err.message || 'Erreur lors de l\'ajout du projet');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setProjectName('');
    setError('');
    onClose();
  };

  return (
    <CModal visible={visible} onClose={handleClose} alignment="center">
      <CModalHeader>
        <CModalTitle>Ajouter un nouveau projet</CModalTitle>
      </CModalHeader>

      <CForm onSubmit={handleSubmit}>
        <CModalBody>
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}

          <div className="mb-3">
            <CFormLabel htmlFor="projectName">
              Nom du projet <span className="text-danger">*</span>
            </CFormLabel>
            <CFormInput
              type="text"
              id="projectName"
              placeholder="Entrez le nom du projet"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              disabled={isSubmitting}
              autoFocus
            />
          </div>
        </CModalBody>

        <CModalFooter>
          <CButton
            color="secondary"
            onClick={handleClose}
            disabled={isSubmitting}
          >
            Annuler
          </CButton>
          <CButton
            color="primary"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Ajout en cours...' : 'Ajouter'}
          </CButton>
        </CModalFooter>
      </CForm>
    </CModal>
  );
}
