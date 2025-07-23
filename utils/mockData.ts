import { OttoScore, CalendarStock } from './types';

export const mockStocks: OttoScore[] = [
  {
    ticker: 'AAPL',
    companyName: 'Apple Inc.',
    score: 87,
    grade: 'A',
    ottosTask: 'Apple shows strong fundamentals with consistent dividend growth, though yield remains modest. Excellent for growth-focused dividend portfolios.',
    dividend: {
      yield: 2.1,
      frequency: 'Quarterly',
      payoutRatio: 25,
      growthRate: 12.5
    },
    factors: {
      growth: 92,
      safety: 88,
      payout: 95,
      consistency: 85,
      valuation: 75
    },
    modifiers: {
      sector: 5,
      momentum: 8,
      quality: 10
    },
    sector: 'Technology',
    beta: 1.15,
    marketCap: 3200000000000
  },
  {
    ticker: 'MSFT',
    companyName: 'Microsoft Corporation',
    score: 91,
    grade: 'A+',
    ottosTask: 'Microsoft demonstrates exceptional dividend reliability with strong balance sheet. A cornerstone holding for conservative dividend investors.',
    dividend: {
      yield: 2.8,
      frequency: 'Quarterly',
      payoutRatio: 35,
      growthRate: 15.2
    },
    factors: {
      growth: 88,
      safety: 95,
      payout: 90,
      consistency: 92,
      valuation: 82
    },
    modifiers: {
      sector: 8,
      momentum: 6,
      quality: 10
    },
    sector: 'Technology',
    beta: 0.95,
    marketCap: 2800000000000
  },
  {
    ticker: 'JNJ',
    companyName: 'Johnson & Johnson',
    score: 85,
    grade: 'A-',
    ottosTask: 'J&J offers defensive characteristics with 60+ years of dividend increases. Ideal for risk-averse investors seeking stability.',
    dividend: {
      yield: 3.2,
      frequency: 'Quarterly',
      payoutRatio: 45,
      growthRate: 5.8
    },
    factors: {
      growth: 75,
      safety: 95,
      payout: 88,
      consistency: 98,
      valuation: 85
    },
    modifiers: {
      sector: 3,
      momentum: -2,
      quality: 9
    },
    sector: 'Healthcare',
    beta: 0.68,
    marketCap: 450000000000
  },
  {
    ticker: 'REALTY',
    companyName: 'Realty Income Corp',
    score: 79,
    grade: 'B+',
    ottosTask: 'The Monthly Dividend Company offers attractive yield with solid real estate fundamentals. Great for income-focused portfolios.',
    dividend: {
      yield: 5.8,
      frequency: 'Monthly',
      payoutRatio: 75,
      growthRate: 3.2
    },
    factors: {
      growth: 65,
      safety: 82,
      payout: 78,
      consistency: 88,
      valuation: 75
    },
    modifiers: {
      sector: 0,
      momentum: 2,
      quality: 7
    },
    sector: 'REITs',
    beta: 0.72,
    marketCap: 85000000000
  },
  {
    ticker: 'SCHD',
    companyName: 'Schwab US Dividend Equity ETF',
    score: 83,
    grade: 'A-',
    ottosTask: 'Excellent diversified dividend ETF with low fees and strong track record. Perfect core holding for dividend portfolios.',
    dividend: {
      yield: 3.6,
      frequency: 'Quarterly',
      payoutRatio: 65,
      growthRate: 8.5
    },
    factors: {
      growth: 78,
      safety: 90,
      payout: 85,
      consistency: 82,
      valuation: 88
    },
    modifiers: {
      sector: 5,
      momentum: 4,
      quality: 8
    },
    sector: 'ETFs',
    beta: 1.02,
    marketCap: 65000000000
  }
];

export const calendarStocks: CalendarStock[] = [
  {
    ticker: 'AAPL',
    companyName: 'Apple Inc.',
    score: 87,
    yield: 2.1,
    paymentMonths: [3, 6, 9, 12]
  },
  {
    ticker: 'MSFT',
    companyName: 'Microsoft Corporation',
    score: 91,
    yield: 2.8,
    paymentMonths: [2, 5, 8, 11]
  },
  {
    ticker: 'JNJ',
    companyName: 'Johnson & Johnson',
    score: 85,
    yield: 3.2,
    paymentMonths: [1, 4, 7, 10]
  }
];