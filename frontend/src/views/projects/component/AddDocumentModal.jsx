import React, { useState, useRef } from 'react';

export default function AddDocumentModal({ visible, onClose, onSubmit, projectName }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (file) => {
    if (file) {
      // Check file size (max 25MB)
      const maxSize = 25 * 1024 * 1024; // 25MB
      if (file.size > maxSize) {
        setError('La taille du fichier ne doit pas dépasser 25 Mo');
        setSelectedFile(null);
        return;
      }

      setSelectedFile(file);
      setError('');
    }
  };

  const handleInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileChange(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileChange(file);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setError('Veuillez sélectionner un document');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      await onSubmit(selectedFile);
      setSelectedFile(null);
      onClose();
    } catch (err) {
      setError(err.message || "Erreur lors de l'ajout du document");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setError('');
    setIsDragging(false);
    onClose();
  };

  if (!visible) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="modal-backdrop fade show"
        onClick={handleClose}
        style={{ zIndex: 1050 }}
      ></div>

      {/* Modal */}
      <div
        className="modal fade show d-block"
        tabIndex="-1"
        style={{ zIndex: 1055 }}
      >
        <div className="modal-dialog modal-dialog-centered">
          <div
            className="modal-content"
            style={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 40px rgba(0,0,0,0.12)' }}
          >
            <form onSubmit={handleSubmit}>
              <div className="modal-body" style={{ padding: '24px 28px' }}>
                {/* Header */}
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h5 className="mb-0" style={{ fontWeight: 700, color: '#0B1849' }}>
                    Upload file
                  </h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={handleClose}
                    disabled={isSubmitting}
                  ></button>
                </div>

                {/* Project Info (optionnel, discret) */}
                {projectName && (
                  <div
                    className="mb-3"
                    style={{ fontSize: '13px', color: '#6b7280' }}
                  >
                    Projet : <strong style={{ color: '#0B1849' }}>{projectName}</strong>
                  </div>
                )}

                {/* Error Message */}
                {error && (
                  <div className="alert alert-danger py-2" role="alert" style={{ fontSize: '13px' }}>
                    {error}
                  </div>
                )}

                {/* Drag & Drop Zone */}
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={handleBrowseClick}
                  style={{
                    border: `2px dashed ${isDragging ? '#00044bff' : '#3b82f6'}`,
                    borderRadius: '10px',
                    backgroundColor: '#eef4ff',
                    cursor: 'pointer',
                    minHeight: '190px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.2s ease',
                    textAlign: 'center',
                    padding: '20px',
                  }}
                >
                 <input
                        ref={fileInputRef}
                        type="file"
                        className="d-none"
                        onChange={handleInputChange}
                        disabled={isSubmitting}
                        accept=".pdf,.doc,.docx,.ppt,.pptx,.md"
                      />

                  {selectedFile ? (
                    <>
                      <i
                        className="bi bi-file-earmark-check"
                        style={{ fontSize: '2.4rem', color: '#00044bff' }}
                      ></i>
                      <p className="mt-3 mb-1 fw-bold" style={{ color: '#0B1849' }}>
                        {selectedFile.name}
                      </p>
                      <small className="text-muted">
                        {(selectedFile.size / 1024).toFixed(2)} KB
                      </small>
                      <p className="mt-2 mb-0 small" style={{ color: '#6b7280' }}>
                        Cliquez pour changer de fichier
                      </p>
                    </>
                  ) : (
                    <>
                      <i
                        className="bi bi-cloud-arrow-up"
                        style={{ fontSize: '2.4rem', color: '#00044bff' }}
                      ></i>
                      <p className="mt-3 mb-0" style={{ color: '#374151' }}>
                        Drag &amp; Drop your files or{' '}
                        <span style={{ color: '#00044bff', textDecoration: 'underline', fontWeight: 600 }}>
                          Browse
                        </span>
                      </p>
                    </>
                  )}
                </div>

                {/* Format Info */}
                <div
                  className="d-flex justify-content-between align-items-center mt-3"
                  style={{ fontSize: '13px', color: '#6b7280' }}
                >
                  <span>Supported formats:PDF, doc ,pptx , md </span>
                  <span>Maximum size: 25MB</span>
                </div>
              </div>

              {/* Footer */}
              <div
                className="d-flex justify-content-end"
                style={{ padding: '0 28px 24px' }}
              >
                <button
                  type="submit"
                  className="btn text-white fw-semibold"
                  style={{
                    backgroundColor: '#00044bff',
                    borderColor: '#00044bff',
                    borderRadius: '8px',
                    padding: '8px 22px',
                  }}
                  disabled={isSubmitting || !selectedFile}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Upload en cours...
                    </>
                  ) : (
                    'Upload'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
