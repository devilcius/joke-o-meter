import MockAdapter from 'axios-mock-adapter';
import { fetchJokometiansRanking } from '../jokometians_ranking';
import { API_BASE_URL, axiosInstance } from '../axios_instance';

const mockAdapter = new MockAdapter(axiosInstance);

describe('Jakometians ranking API', () => {

  it('gets jakometians ranking', async () => {
    const mockData = [
      {
        "name": "ETHNICITY",
        "score": 28,
        "image_url": "/assets/images/jokometians/image_ethnicity.svg"
      }
    ];
    mockAdapter.onGet(`${API_BASE_URL}/jokometian-rankings/`).reply(200, mockData);

    const response = await fetchJokometiansRanking();
    expect(response.data).toEqual(mockData);
  });
});