"use client";

import { useState, useEffect, useRef } from 'react';
import { Message } from './types';
import { AlertTriangle, Target, Hash, Goal, Trophy } from 'lucide-react';
import ChatMessage from './components/ChatMessage';

const CHAMPIONSHIPS = {
  Football: ["Ligue 1", "Premier League", "La Liga"],
};

const MATCHES = {
  "Ligue 1": ["Marseille vs PSG", "Lyon vs Monaco", "Nice vs Rennes"],
};

const SPORTS = ["Football", "Basketball", "Tennis", "Baseball", "Formule 1", "Rugby"];

export default function Page() {
  const [messages, setMessages] = useState<Message[]>([
    { id: crypto.randomUUID(), content: 'Bonjour! Je suis Bêt, votre assistant de paris sportifs. Sélectionnez un sport pour commencer.', role: 'assistant' }
  ]);

  const [selectedSport, setSelectedSport] = useState<string | null>(null);
  const [selectedChampionship, setSelectedChampionship] = useState<string | null>(null);
  const [selectedMatch, setSelectedMatch] = useState<string | null>(null);
  const [selectedBetType, setSelectedBetType] = useState<string | null>(null);
  const [chatEnabled, setChatEnabled] = useState(false);
  const [userInput, setUserInput] = useState("");

  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatContainerRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (selectedSport && selectedChampionship && selectedMatch && selectedBetType) {
      setChatEnabled(true);
    }
  }, [selectedSport, selectedChampionship, selectedMatch, selectedBetType]);

  const addMessage = (content: string, role: "user" | "assistant") => {
    setMessages((prev) => [...prev, { id: crypto.randomUUID(), content, role }]);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar avec "Football" en bouton et les autres sports en texte simple */}
      <div className="w-64 bg-purple-700 text-white p-4">
        <h2 className="text-lg font-bold mb-4">Bêt</h2>
        <div className="space-y-2">
          {SPORTS.map((sport) => {
            const isFootball = sport === "Football";

            return isFootball ? (
              <button
                key={sport}
                className="w-full p-2 rounded-lg text-left bg-purple-600 text-white hover:bg-purple-500"
                onClick={() => {
                  setSelectedSport(sport);
                  setSelectedChampionship(null);
                  setSelectedMatch(null);
                  setSelectedBetType(null);
                  setChatEnabled(false);
                  addMessage(`J'ai sélectionné le sport : ${sport}`, "user");
                  addMessage("Sélectionnez un championnat :", "assistant");
                }}
              >
                {sport}
              </button>
            ) : (
              <div key={sport} className="text-gray-400 cursor-default">
                {sport}
              </div>
            );
          })}
        </div>
      </div>

      <main className="flex-1 flex flex-col">
        <div className="bg-violet-100 p-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-violet-600" />
          <p className="text-sm text-violet-900">
            Les paris peuvent être addictifs. Pariez de manière responsable et respectez la législation locale.
          </p>
        </div>

        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {/* Étape 1 : Sélection du championnat */}
          {selectedSport && !selectedChampionship && (
            <div className="grid grid-cols-2 gap-4">
              {CHAMPIONSHIPS[selectedSport].map((championship, index) => (
                <button
                  key={`${selectedSport}-${championship}-${index}`}
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
              {MATCHES[selectedChampionship]?.map((match, index) => (
                <button
                  key={`${selectedChampionship}-${match}-${index}`}
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
              ].map(({ name, icon }, index) => (
                <button
                  key={`${selectedMatch}-${name}-${index}`}
                  className="flex flex-col items-center p-4 rounded-lg bg-purple-100 hover:bg-purple-200"
                  onClick={() => {
                    setSelectedBetType(name);
                    addMessage(`J'ai sélectionné le pari : ${name}`, "user");
                    addMessage("Vous pouvez maintenant discuter avec moi !", "assistant");
                  }}
                >
                  {icon}
                  <span className="mt-2 font-medium">{name}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div ref={chatContainerRef} />

        {/* ✅ Barre de discussion activée uniquement après avoir sélectionné un pari */}
        {chatEnabled && (
          <div className="p-4 border-t bg-white flex items-center">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Écrivez un message..."
              className="flex-1 p-2 border rounded-lg"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  if (userInput.trim() !== "") {
                    addMessage(userInput, "user");
                    setUserInput("");
                  }
                }
              }}
            />
            <button
              onClick={() => {
                if (userInput.trim() !== "") {
                  addMessage(userInput, "user");
                  setUserInput("");
                }
              }}
              className="ml-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Envoyer
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
