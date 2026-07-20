
import api from '../../axios/api'


export const getDocumentsByProjectId = async (id) => {
  try {
    const { data } = await api.get(`/documents/list/${id}`);

    console.log("Response :", data);
    console.log("Documents :", data.documents);

    return Array.isArray(data.documents) ? data.documents : [];
  } catch (error) {
    console.error(`Error fetching documents for project ${id}:`, error);
    return [];
  }
};



export const addDocument = async (projectId, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_id', projectId);

    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('Document upload response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error uploading document:', error);
    throw error;
  }
};

export const delete_document = async (document_id) => {
  try {
    const response = await api.delete(`/documents/${document_id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting document:', error);
    throw error;
  }
};



export default {
  getDocumentsByProjectId,
  addDocument,
  delete_document
}
