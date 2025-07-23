export interface OttoScore {
  ticker: string;
  companyName: string;
  score: number;
  grade: 'A+' | 'A' | 'A-' | 'B+' | 'B' | 'B-' | 'C+' | 'C' | 'C-' | 'D' | 'F';
  ottosTask: string;
  dividend: {
    yield: number;
    frequency: 'Monthly' | 'Quarterly' | 'Semi-Annual' | 'Annual';
    payoutRatio: number;
    growthRate: number;
  };
  factors: {
    growth: number;
    safety: number;
    payout: number;
    consistency: number;
    valuation: number;
  };
  modifiers: {
    sector: number;
    momentum: number;
    quality: number;
  };
  sector: string;
  beta: number;
  marketCap: number;
}

export interface ScreenerFilters {
  minYield?: number;
  maxYield?: number;
  sectors?: string[];
  frequency?: string[];
  maxBeta?: number;
  minScore?: number;
  maxScore?: number;
}

export interface CalendarStock {
  ticker: string;
  companyName: string;
  score: number;
  yield: number;
  paymentMonths: number[];
}

export interface User {
  uid: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
}