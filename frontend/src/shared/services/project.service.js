
import api from '../../axios/api'


export const getAllProjects = async () => {
  const response = await api.get('/projects')
  console.log('API Response:', response)
  console.log('Response.data:', response.data)
  console.log('Is Array?', Array.isArray(response.data))
  
  // If the API returns {data: [...]} structure, access response.data.data
  // Otherwise, response.data should already be the array
  const projects = Array.isArray(response.data) ? response.data : response.data.data
  console.log('Final projects:', projects)
  return projects
} 



export const addProject= async(project)=>{
  const response =await api.post('/projects',project)
  return response.data
}



export default {
  getAllProjects,
  addProject
}
