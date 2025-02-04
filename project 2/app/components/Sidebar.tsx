'use client';

import { Sport } from '../types';
import { FolderRoot as Football, ShoppingBasket as Basketball, Trophy, Baseline as Baseball, Car, Flag } from 'lucide-react';

const sports: { id: Sport; icon: React.ReactNode }[] = [
  { id: 'Football', icon: <Football className="w-5 h-5" /> },
  { id: 'Basketball', icon: <Basketball className="w-5 h-5" /> },
  { id: 'Tennis', icon: <Trophy className="w-5 h-5" /> },
  { id: 'Baseball', icon: <Baseball className="w-5 h-5" /> },
  { id: 'Formule 1', icon: <Car className="w-5 h-5" /> },
  { id: 'Rugby', icon: <Flag className="w-5 h-5" /> },
];

export default function Sidebar({ onSportSelect }: { onSportSelect: (sport: Sport) => void }) {
  return (
    <div className="w-64 bg-violet-600 text-white h-screen p-4">
      <div className="flex items-center gap-2 mb-8">
        <Trophy className="w-6 h-6" />
        <h1 className="text-xl font-bold">Bêt</h1>
      </div>
      
      <div className="space-y-2">
        {sports.map((sport) => (
          <button
            key={sport.id}
            onClick={() => onSportSelect(sport.id)}
            className="flex items-center gap-3 p-3 w-full text-left rounded-lg hover:bg-violet-700 transition-colors"
          >
            {sport.icon}
            <span>{sport.id}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
