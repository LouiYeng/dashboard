import client from './client';
import type { LoginRequest, TokenResponse } from '../types/auth';

export const authApi = {
  login: (data: LoginRequest) =>
    client.post<TokenResponse>('/auth/login', data).then(r => r.data),

  refresh: (refreshToken: string) =>
    client.post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken }).then(r => r.data),

  getMe: () =>
    client.get('/auth/me').then(r => r.data),
};
