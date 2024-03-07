import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import { fetchJokometian } from '../jokometians';

const mockAdapter = new MockAdapter(axios);
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

describe('Jakometians API', () => {

  it('gets jakometians successfully', async () => {
    const uuid = '123e4567-e89b-12d3-a456-426614174000'
    const mockData = { 
      "name": "Jakometian 1",
      "description": "Jakometian 1 description",
      "image_url": "https://www.jakometian1.com/image.jpg"
    };
    mockAdapter.onGet(`${API_BASE_URL}/jokometians/${uuid}/`).reply(200, mockData);

    const response = await fetchJokometian(uuid);
    expect(response.data).toEqual(mockData);
  } );
});