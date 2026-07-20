/**
 * FAQ Service
 * Handles all FAQ-related data operations
 * Ready to be replaced with API calls
 */

import { createFaq } from '../models/Faq.model'

// Mock data
let mockFaqs = [
  {
    id: '1',
    question: 'Comment réinitialiser mon mot de passe ?',
    reponse:
      'Cliquez sur "Mot de passe oublié" sur la page de connexion, puis suivez les instructions envoyées par email.',
    categorie: 'Compte',
  },
  {
    id: '2',
    question: 'Comment contacter le support technique ?',
    reponse:
      'Vous pouvez nous contacter par email à support@example.com ou par téléphone au 01 23 45 67 89.',
    categorie: 'Support',
  },
  {
    id: '3',
    question: "Quelles sont les heures d'ouverture ?",
    reponse: 'Notre service est disponible du lundi au vendredi de 9h à 18h.',
    categorie: 'Général',
  },
]

/**
 * Get all FAQs
 * @returns {Promise<Faq[]>}
 */
export const getAllFaqs = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([...mockFaqs])
    }, 100)
  })
}

/**
 * Get FAQ by ID
 * @param {string} id
 * @returns {Promise<Faq|null>}
 */
export const getFaqById = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const faq = mockFaqs.find((f) => f.id === id)
      resolve(faq || null)
    }, 100)
  })
}

/**
 * Create new FAQ
 * @param {Object} faqData
 * @returns {Promise<Faq>}
 */
export const createNewFaq = async (faqData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const newFaq = createFaq({
        ...faqData,
        id: Date.now().toString(),
      })
      mockFaqs.push(newFaq)
      resolve(newFaq)
    }, 100)
  })
}

/**
 * Update existing FAQ
 * @param {string} id
 * @param {Object} faqData
 * @returns {Promise<Faq|null>}
 */
export const updateFaq = async (id, faqData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const index = mockFaqs.findIndex((f) => f.id === id)
      if (index !== -1) {
        mockFaqs[index] = {
          ...mockFaqs[index],
          ...faqData,
          id, // Preserve ID
        }
        resolve(mockFaqs[index])
      } else {
        resolve(null)
      }
    }, 100)
  })
}

/**
 * Delete FAQ
 * @param {string} id
 * @returns {Promise<boolean>}
 */
export const deleteFaq = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const initialLength = mockFaqs.length
      mockFaqs = mockFaqs.filter((f) => f.id !== id)
      resolve(mockFaqs.length < initialLength)
    }, 100)
  })
}

export default {
  getAllFaqs,
  getFaqById,
  createNewFaq,
  updateFaq,
  deleteFaq,
}
