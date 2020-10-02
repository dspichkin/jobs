import request from '@/utils/request'

export default function loadAPISpecialityData (params) {
  const url = '/api/speciality/'
  return request({
    url,
    params,
    method: 'get'
  })
}
