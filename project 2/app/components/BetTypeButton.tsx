'use client';

import { BetType } from '../types';
import { Target, Hash, Goal, Trophy } from 'lucide-react';

interface BetTypeButtonProps {
  type: BetType;
  onClick: (type: BetType) => void;
}

const icons = {
  'Buteur': Target,
  'Score Exact': Hash,
  'Nombre de Buts': Goal,
  'Vainqueur': Trophy,
};

export default function BetTypeButton({ type, onClick }: BetTypeButtonProps) {
  const Icon = icons[type];
  
  return (
    <button
      onClick={() => onClick(type)}
      className="flex-1 p-4 bg-violet-100 hover:bg-violet-200 rounded-lg transition-colors flex flex-col items-center gap-2"
    >
      <Icon className="w-6 h-6 text-violet-600" />
      <span className="text-sm text-violet-900">{type}</span>
    </button>
  );
}