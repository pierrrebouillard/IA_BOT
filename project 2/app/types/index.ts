export type Sport = 'Football' | 'Basketball' | 'Tennis' | 'Baseball' | 'Formule 1' | 'Rugby';

export type League = 'Ligue 1' | 'Premier League' | 'La Liga' | 'Champions League';

export type BetType = 'Buteur' | 'Score Exact' | 'Nombre de Buts' | 'Vainqueur';

export interface Message {
  id: string;
  content: string;
  role: 'assistant' | 'user';
}

export interface Bet {
  sport: Sport;
  league?: League;
  match?: string;
  betType?: BetType;
  prediction?: string;
}