import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import { postJokes, fetchJokes } from '../jokes';

const mockAdapter = new MockAdapter(axios);
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

describe('Jokes API', () => {

  beforeEach(() => {
    mockAdapter.reset();
  });

  it('posts jokes successfully', async () => {
    const mockResponse = { success: true };
    const jokes = [
      {
        "joke": 1,
        "liked": true,
        "session": "06fc7dc7-ab0a-43e9-b8c2-b9a9d5d4c4af",
      },
      {
        "joke": 2,
        "liked": false,
        "session": "06fc7dc7-ab0a-43e9-b8c2-b9a9d5d4c4af",
      }
    ]
    mockAdapter.onPost(`${API_BASE_URL}/evaluate-jokes/`. jokes).reply(201, mockResponse);

    const response = await postJokes(jokes);
    expect(response.data).toEqual(mockResponse);
  });

  it('handles error when posting jokes', async () => {
    const mockError = { error: 'Error occurred during posting jokes' };
    mockAdapter.onPost(`${API_BASE_URL}/evaluate-jokes/`).reply(500, mockError);

    const response = await postJokes([]);
    expect(response.data).toEqual(mockError);
  });

  it('Gets all jokes successfully', async () => {
    const mockData = [
      {
        "id": "1",
        "content": "joke 1",
        "session": "06fc7dc7-ab0a-43e9-b8c2-b9a9d5d4c4af",
      },
      {
        "id": "2",
        "content": "joke 2",
        "session": "06fc7dc7-ab0a-43e9-b8c2-b9a9d5d4c4af",
      }
    ];
    mockAdapter.onGet(`${API_BASE_URL}/jokes/`).reply(200, mockData);

    const response = await fetchJokes();
    expect(response.data).toEqual(mockData);
  });
});