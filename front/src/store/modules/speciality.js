import loadAPISpecialityData from '@/api/api_speciality'

const speciality = {
  namespaced: true,
  state: {
    speciality_data: []
  },
  mutations: {},
  actions: {
    loadSpecialityData (_, data) {
      return loadAPISpecialityData(data)
    }
  }
}

export default speciality
