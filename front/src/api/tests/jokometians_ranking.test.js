import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import { fetchJokometiansRanking } from '../jokometians_ranking';

const mockAdapter = new MockAdapter(axios);
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

describe('Jakometians ranking API', () => {

  it('gets jakometians ranking', async () => {
    const mockData = [
      {
        "name": "ETHNICITY",
        "score": 28,
        "image_url": "/static/images/jokometians/image_ethnicity.svg"
      }
    ];
    mockAdapter.onGet(`${API_BASE_URL}/jokometian-rankings/`).reply(200, mockData);

    const response = await fetchJokometiansRanking();
    expect(response.data).toEqual(mockData);
  });
});