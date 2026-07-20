/**
 * FAQ Management Component
 *
 * CRUD interface for managing FAQs with mock data.
 * Features:
 * - List all FAQs
 * - Add new FAQ
 * - Edit existing FAQ
 * - Delete FAQ
 *
 * @component
 */

import React, { useState } from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CFormSelect,
  CFormTextarea,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CBadge,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPencil, cilTrash, cilPlus } from '@coreui/icons'

const Faq = () => {
  // Mock data pour les FAQs
  const [faqs, setFaqs] = useState([
    {
      id: 1,
      question: 'Comment réinitialiser mon mot de passe ?',
      reponse:
        'Cliquez sur "Mot de passe oublié" sur la page de connexion, puis suivez les instructions envoyées par email.',
      categorie: 'Compte',
    },
    {
      id: 2,
      question: 'Comment contacter le support technique ?',
      reponse:
        'Vous pouvez nous contacter par email à support@example.com ou par téléphone au 01 23 45 67 89.',
      categorie: 'Support',
    },
    {
      id: 3,
      question: "Quelles sont les heures d'ouverture ?",
      reponse: 'Notre service est disponible du lundi au vendredi de 9h à 18h.',
      categorie: 'Général',
    },
  ])

  const [showModal, setShowModal] = useState(false)
  const [editMode, setEditMode] = useState(false)
  const [currentFaq, setCurrentFaq] = useState({
    id: null,
    question: '',
    reponse: '',
    categorie: 'Général',
  })

  const categories = ['Général', 'Compte', 'Support', 'Facturation', 'Technique']

  const categoryColors = {
    Général: 'primary',
    Compte: 'success',
    Support: 'info',
    Facturation: 'warning',
    Technique: 'danger',
  }

  // Ouvrir le modal pour ajouter une FAQ
  const handleAdd = () => {
    setEditMode(false)
    setCurrentFaq({
      id: null,
      question: '',
      reponse: '',
      categorie: 'Général',
    })
    setShowModal(true)
  }

  // Ouvrir le modal pour éditer une FAQ
  const handleEdit = (faq) => {
    setEditMode(true)
    setCurrentFaq({ ...faq })
    setShowModal(true)
  }

  // Sauvegarder la FAQ (ajouter ou modifier)
  const handleSave = () => {
    if (editMode) {
      setFaqs(faqs.map((faq) => (faq.id === currentFaq.id ? currentFaq : faq)))
    } else {
      const newFaq = {
        ...currentFaq,
        id: Math.max(...faqs.map((f) => f.id)) + 1,
      }
      setFaqs([...faqs, newFaq])
    }
    setShowModal(false)
  }

  // Supprimer une FAQ
  const handleDelete = (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette FAQ ?')) {
      setFaqs(faqs.filter((faq) => faq.id !== id))
    }
  }

  // Gérer les changements dans le formulaire
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setCurrentFaq({ ...currentFaq, [name]: value })
  }

  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardHeader className="d-flex justify-content-between align-items-center">
            <strong>Gestion des FAQ</strong>
            <CButton color="primary" onClick={handleAdd}>
              <CIcon icon={cilPlus} className="me-2" />
              Ajouter une FAQ
            </CButton>
          </CCardHeader>
          <CCardBody>
            <CTable hover responsive>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell scope="col">#</CTableHeaderCell>
                  <CTableHeaderCell scope="col">Question</CTableHeaderCell>
                  <CTableHeaderCell scope="col">Réponse</CTableHeaderCell>
                  <CTableHeaderCell scope="col">Catégorie</CTableHeaderCell>
                  <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {faqs.map((faq) => (
                  <CTableRow key={faq.id}>
                    <CTableHeaderCell scope="row">{faq.id}</CTableHeaderCell>
                    <CTableDataCell>{faq.question}</CTableDataCell>
                    <CTableDataCell>
                      {faq.reponse.length > 80
                        ? `${faq.reponse.substring(0, 80)}...`
                        : faq.reponse}
                    </CTableDataCell>
                    <CTableDataCell>
                      <CBadge color={categoryColors[faq.categorie]}>{faq.categorie}</CBadge>
                    </CTableDataCell>
                    <CTableDataCell>
                      <CButton
                        color="info"
                        size="sm"
                        className="me-2"
                        onClick={() => handleEdit(faq)}
                      >
                        <CIcon icon={cilPencil} />
                      </CButton>
                      <CButton color="danger" size="sm" onClick={() => handleDelete(faq.id)}>
                        <CIcon icon={cilTrash} />
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                ))}
              </CTableBody>
            </CTable>
          </CCardBody>
        </CCard>
      </CCol>

      {/* Modal pour ajouter/éditer une FAQ */}
      <CModal visible={showModal} onClose={() => setShowModal(false)} size="lg">
        <CModalHeader>
          <CModalTitle>{editMode ? 'Modifier la FAQ' : 'Ajouter une FAQ'}</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm>
            <div className="mb-3">
              <CFormLabel htmlFor="question">Question</CFormLabel>
              <CFormInput
                type="text"
                id="question"
                name="question"
                value={currentFaq.question}
                onChange={handleInputChange}
                placeholder="Entrez la question"
              />
            </div>
            <div className="mb-3">
              <CFormLabel htmlFor="reponse">Réponse</CFormLabel>
              <CFormTextarea
                id="reponse"
                name="reponse"
                rows={4}
                value={currentFaq.reponse}
                onChange={handleInputChange}
                placeholder="Entrez la réponse"
              />
            </div>
            <div className="mb-3">
              <CFormLabel htmlFor="categorie">Catégorie</CFormLabel>
              <CFormSelect
                id="categorie"
                name="categorie"
                value={currentFaq.categorie}
                onChange={handleInputChange}
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </CFormSelect>
            </div>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setShowModal(false)}>
            Annuler
          </CButton>
          <CButton color="primary" onClick={handleSave}>
            {editMode ? 'Mettre à jour' : 'Ajouter'}
          </CButton>
        </CModalFooter>
      </CModal>
    </CRow>
  )
}

export default Faq
