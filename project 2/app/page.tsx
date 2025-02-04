'use client';

import { useState, useEffect, useRef } from 'react';
import { Message, Bet, BetType } from './types';
import { AlertTriangle, Target, Hash, Goal, Trophy } from 'lucide-react'; // ✅ Ajout des icônes
import ChatMessage from './components/ChatMessage';
import Sidebar from './components/Sidebar';

const CHAMPIONSHIPS: { [key: string]: string[] } = {
  Football: ["Ligue 1", "Premier League", "La Liga"],
  Basketball: ["NBA", "EuroLeague"],
  Tennis: ["Roland Garros", "Wimbledon"],
  Baseball: ["MLB", "Nippon League"],
  "Formule 1": ["Grand Prix Monaco", "Grand Prix Italie"],
  Rugby: ["Top 14", "Six Nations"]
};

// ✅ Liste des matchs par championnat
const MATCHES: { [key: string]: string[] } = {
  "Ligue 1": ["Marseille vs PSG", "Lyon vs Monaco", "Nice vs Rennes"],
  "Premier League": ["Manchester United vs Liverpool", "Chelsea vs Arsenal"],
  "La Liga": ["Real Madrid vs Barcelona", "Atletico Madrid vs Sevilla"],
  NBA: ["Lakers vs Celtics", "Warriors vs Heat"],
  EuroLeague: ["Barcelona vs CSKA Moscow", "Olympiacos vs Fenerbahce"],
  "Roland Garros": ["Djokovic vs Nadal", "Alcaraz vs Tsitsipas"],
  Wimbledon: ["Federer vs Murray", "Medvedev vs Zverev"],
  MLB: ["Yankees vs Red Sox", "Dodgers vs Cubs"],
  "Nippon League": ["Giants vs Tigers"],
  "Grand Prix Monaco": ["Verstappen vs Hamilton"],
  "Grand Prix Italie": ["Leclerc vs Sainz"],
  "Top 14": ["Toulouse vs La Rochelle", "Racing 92 vs Stade Français"],
  "Six Nations": ["France vs Angleterre", "Irlande vs Pays de Galles"]
};

export default function Page() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', content: 'Bonjour! Je suis Bêt, votre assistant de paris sportifs. Sélectionnez un sport pour commencer.', role: 'assistant' }
  ]);

  const [selectedSport, setSelectedSport] = useState<string | null>(null);
  const [selectedChampionship, setSelectedChampionship] = useState<string | null>(null);
  const [selectedMatch, setSelectedMatch] = useState<string | null>(null);
  const [selectedBetType, setSelectedBetType] = useState<string | null>(null);
  const [prediction, setPrediction] = useState("");

  const chatContainerRef = useRef<HTMLDivElement>(null);

  // 🔄 Scroller automatiquement en bas après chaque mise à jour
  useEffect(() => {
    chatContainerRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🔹 Fonction pour ajouter un message au chat
  const addMessage = (content: string, role: "user" | "assistant") => {
    setMessages((prev) => [...prev, { id: Date.now().toString(), content, role }]);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar onSportSelect={(sport) => {
        setSelectedSport(sport);
        setSelectedChampionship(null);
        setSelectedMatch(null);
        setSelectedBetType(null);
        setPrediction("");
        addMessage(`J'ai sélectionné le sport : ${sport}`, "user");
        addMessage("Sélectionnez un championnat :", "assistant");
      }} />

      <main className="flex-1 flex flex-col">
        {/* Avertissement */}
        <div className="bg-violet-100 p-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-violet-600" />
          <p className="text-sm text-violet-900">
            Les paris peuvent être addictifs. Pariez de manière responsable et respectez la législation locale.
          </p>
        </div>

        {/* 🔹 Zone de discussion */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {/* Étape 1 : Sélection du championnat */}
          {selectedSport && !selectedChampionship && (
            <div className="grid grid-cols-2 gap-4">
              {CHAMPIONSHIPS[selectedSport].map((championship) => (
                <button
                  key={championship}
                  className="p-2 bg-gray-200 rounded-lg hover:bg-gray-300"
                  onClick={() => {
                    setSelectedChampionship(championship);
                    addMessage(`J'ai sélectionné le championnat : ${championship}`, "user");
                    addMessage("Sélectionnez un match :", "assistant");
                  }}
                >
                  {championship}
                </button>
              ))}
            </div>
          )}

          {/* Étape 2 : Sélection du match */}
          {selectedChampionship && !selectedMatch && (
            <div className="grid grid-cols-2 gap-4">
              {MATCHES[selectedChampionship]?.map((match) => (
                <button
                  key={match}
                  className="p-2 bg-gray-200 rounded-lg hover:bg-gray-300"
                  onClick={() => {
                    setSelectedMatch(match);
                    addMessage(`J'ai sélectionné le match : ${match}`, "user");
                    addMessage("Choisissez un type de pari :", "assistant");
                  }}
                >
                  {match}
                </button>
              ))}
            </div>
          )}

          {/* Étape 3 : Sélection du type de pari */}
          {selectedMatch && !selectedBetType && (
            <div className="grid grid-cols-4 gap-4">
              {[
                { name: "Buteur", icon: <Target className="w-6 h-6 text-purple-600" /> },
                { name: "Score Exact", icon: <Hash className="w-6 h-6 text-purple-600" /> },
                { name: "Nombre de Buts", icon: <Goal className="w-6 h-6 text-purple-600" /> },
                { name: "Vainqueur", icon: <Trophy className="w-6 h-6 text-purple-600" /> },
              ].map(({ name, icon }) => (
                <button
                  key={name}
                  className="flex flex-col items-center p-4 rounded-lg bg-purple-100 hover:bg-purple-200"
                  onClick={() => {
                    setSelectedBetType(name);
                    addMessage(`J'ai sélectionné le pari : ${name}`, "user");
                    addMessage("Entrez votre prédiction :", "assistant");
                  }}
                >
                  {icon}
                  <span className="mt-2 font-medium">{name}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Scroller en bas pour voir les nouveaux messages */}
        <div ref={chatContainerRef} />
      </main>
    </div>
  );
}
