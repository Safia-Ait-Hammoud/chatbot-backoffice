import React, { useMemo, useState, useEffect } from 'react';


// Fonction pour formater la date
const formatDate = (dateString) => {
  if (!dateString) return '-';
  
  try {
    const date = new Date(dateString);
    
    // Vérifier si la date est valide
    if (isNaN(date.getTime())) return '-';
    
    // Format: JJ/MM/AAAA HH:MM
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${day}/${month}/${year} ${hours}:${minutes}`;
  } catch (error) {
    console.error('Error formatting date:', error);
    return '-';
  }
};

export default function DocumentComponent({
  documents = [],
  pageSize = 8,
  onAdd,
  onView,
  onEdit,
  onDelete,
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  const filteredDocuments = useMemo(() => {
    // Ensure documents is always an array
    const docList = Array.isArray(documents) ? documents : [];
    const term = searchTerm.trim().toLowerCase();

    if (!term) {
      return docList;
    }

    return docList.filter((doc) =>
      doc.name.toLowerCase().includes(term)
    );
  }, [documents, searchTerm]);

  const totalPages = Math.max(
    1,
    Math.ceil(filteredDocuments.length / pageSize)
  );

  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm]);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  const pageDocuments = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredDocuments.slice(start, start + pageSize);
  }, [filteredDocuments, currentPage, pageSize]);

  const goToPage = (page) => {
    if (page < 1 || page > totalPages) {
      return;
    }

    setCurrentPage(page);
  };

  

  return (
    <div>
      <div className="documents-toolbar">
        
        <button
          type="button"
          className="btn btn-sm btn-outline-primary"
          style={{ borderColor: '#0B1849', color: '#0B1849' }}
          onClick={onAdd}
        >
          <i className="bi bi-plus-lg me-1"></i>
          Ajouter un document
        </button>
      </div>

      <table className="table documents-table mb-0">
        <thead>
          <tr>
            <th style={{ width: 36 }}></th>
            <th>Nom du document</th>
            <th style={{ width: 130 }}>Date</th>
            <th style={{ width: 100 }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {pageDocuments.length === 0 ? (
            <tr>
              <td colSpan={4} className="doc-empty">
                Aucun document trouvé.
              </td>
            </tr>
          ) : (
            pageDocuments.map((doc) => (
              <tr key={doc.id}>
                <td>
                  <i className="bi bi-file-earmark-pdf"></i>
                </td>

                <td>{doc.filename}</td>

                <td>{doc.created_at}</td>

                <td>
                  <div className="action-icons">
                    <i
                      className="bi bi-eye"
                      title="Voir"
                      onClick={() => onView(doc)}
                    ></i>

                    <i
                      className="bi bi-pencil"
                      title="Modifier"
                      onClick={() => onEdit(doc)}
                    ></i>

                    <i
                      className="bi bi-trash action-delete"
                      title="Supprimer"
                      onClick={() => onDelete(doc)}
                    ></i>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      <div className="documents-pagination">
        <span className="pagination-info">
          Page {currentPage} sur {totalPages} ({filteredDocuments.length}{' '}
          document{filteredDocuments.length > 1 ? 's' : ''})
        </span>

        <nav>
          <ul className="pagination pagination-sm">
            <li
              className={`page-item ${
                currentPage === 1 ? 'disabled' : ''
              }`}
            >
              <button
                className="page-link"
                onClick={() => goToPage(currentPage - 1)}
              >
                <i className="bi bi-chevron-left"></i>
              </button>
            </li>

            <li
              className={`page-item ${
                currentPage === totalPages ? 'disabled' : ''
              }`}
            >
              <button
                className="page-link"
                onClick={() => goToPage(currentPage + 1)}
              >
                <i className="bi bi-chevron-right"></i>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}