import axios from 'axios';
import { OttoScore, ScreenerFilters } from './types';
import { mockStocks } from './mockData';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.ottotools.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const ottoAPI = {
  // Get OttoScore for a specific ticker
  async getScore(ticker: string): Promise<OttoScore> {
    try {
      const response = await api.get(`/api/score?ticker=${ticker}`);
      return response.data;
    } catch (error) {
      // Fallback to mock data for development
      console.log('Using mock data for:', ticker);
      const mockStock = mockStocks.find(s => s.ticker === ticker.toUpperCase());
      if (mockStock) {
        return mockStock;
      }
      throw new Error(`Stock ${ticker} not found`);
    }
  },

  // Screen stocks based on filters
  async screenStocks(filters: ScreenerFilters): Promise<OttoScore[]> {
    try {
      const response = await api.post('/api/screen', filters);
      return response.data;
    } catch (error) {
      // Fallback to filtered mock data
      console.log('Using mock data for screening');
      return mockStocks.filter(stock => {
        if (filters.minYield && stock.dividend.yield < filters.minYield) return false;
        if (filters.maxYield && stock.dividend.yield > filters.maxYield) return false;
        if (filters.sectors && filters.sectors.length > 0 && !filters.sectors.includes(stock.sector)) return false;
        if (filters.frequency && filters.frequency.length > 0 && !filters.frequency.includes(stock.dividend.frequency)) return false;
        if (filters.maxBeta && stock.beta > filters.maxBeta) return false;
        if (filters.minScore && stock.score < filters.minScore) return false;
        if (filters.maxScore && stock.score > filters.maxScore) return false;
        return true;
      });
    }
  },

  // Compare multiple stocks
  async compareStocks(tickers: string[]): Promise<OttoScore[]> {
    try {
      const response = await api.post('/api/compare', { tickers });
      return response.data;
    } catch (error) {
      // Fallback to mock data
      console.log('Using mock data for comparison');
      return mockStocks.filter(stock => 
        tickers.map(t => t.toUpperCase()).includes(stock.ticker)
      );
    }
  },

  // Get calendar suggestions
  async getCalendarSuggestions(criteria: any): Promise<any> {
    try {
      const response = await api.post('/api/calendar', criteria);
      return response.data;
    } catch (error) {
      console.log('Using mock data for calendar');
      return {
        suggestions: [
          { ticker: 'AAPL', months: [1, 4, 7, 10] },
          { ticker: 'MSFT', months: [2, 5, 8, 11] },
          { ticker: 'JNJ', months: [3, 6, 9, 12] }
        ]
      };
    }
  }
};

export default api;