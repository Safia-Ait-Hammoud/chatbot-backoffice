import React from 'react'
import { CButton, CModal, CModalBody, CModalFooter, CModalHeader, CModalTitle } from '@coreui/react'

const ConfirmDeleteModal = ({ visible, onClose, onConfirm, title, message }) => {
  return (
    <CModal visible={visible} onClose={onClose}>
      <CModalHeader>
        <CModalTitle>{title || 'Confirmer la suppression'}</CModalTitle>
      </CModalHeader>
      <CModalBody>
        {message || 'Êtes-vous sûr de vouloir supprimer cet élément ?'}
      </CModalBody>
      <CModalFooter>
        <CButton color="secondary" onClick={onClose}>
          Annuler
        </CButton>
        <CButton color="danger" onClick={onConfirm}>
          Supprimer
        </CButton>
      </CModalFooter>
    </CModal>
  )
}

export default ConfirmDeleteModal
