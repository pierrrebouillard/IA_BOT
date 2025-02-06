"use client";


import Head from "next/head";
import { ChevronDownIcon, ClockIcon, PlusCircleIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

export default function Home() {
  const [isFootballOpen, setIsFootballOpen] = useState(false);
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [selectedBetType, setSelectedBetType] = useState(null);

  const leagues = {
    "Premier League": ["Match 1", "Match 2", "Match 3"],
    "La Liga": ["Match 4", "Match 5", "Match 6"],
    "Serie A": ["Match 7", "Match 8", "Match 9"],
    "Bundesliga": ["Match 10", "Match 11", "Match 12"],
    "Ligue 1": ["Match 13", "Match 14", "Match 15"],
  };

  const betTypes = [
    "Résultat du match",
    "Nombre de buts",
    "Équipe qui marque en premier"
  ];

  return (
    <div className="bg-gradient-to-br from-[#150931] to-[#344267] min-h-screen flex flex-col">
      <Head>
        <title>Bet - Chatbot</title>
      </Head>
      <div className="flex flex-row h-screen">
        {/* Sidebar */}
        <div className="w-[285px] bg-gradient-to-b from-[#341479] to-[#5159BB] p-6 text-white flex flex-col">
          <h1 className="text-2xl font-semibold mb-20">Bêt</h1>
          
          <nav className="mb-10">
            <h2 className="text-lg font-semibold">Sports</h2>
            <ul className="mt-3 space-y-4">
              <li className="py-2 cursor-pointer flex items-center justify-between" onClick={() => setIsFootballOpen(!isFootballOpen)}>
                Football <ChevronDownIcon className={`w-5 h-5 inline transition-transform ${isFootballOpen ? 'rotate-180' : ''}`} />
              </li>
              {isFootballOpen && (
                <ul className="ml-4 mt-2 opacity-90">
                  {Object.keys(leagues).map((league) => (
                    <li key={league} className="py-1 cursor-pointer" onClick={() => setSelectedLeague(league)}>
                      {league}
                    </li>
                  ))}
                </ul>
              )}
            </ul>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-16 text-white flex flex-col items-center justify-between">
          <div className="text-center mt-[125px]">
            <h2 className="text-4xl font-semibold">Bêt</h2>
            <p className="mt-4 opacity-80 text-lg">Prenez les meilleures décisions de paris avec Bêt</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
            {/* Example Card - Matches */}
            <div className="bg-gradient-to-br from-[#2B3257] to-[#344267] p-8 rounded-xl border border-[#4F5D84] shadow-lg shadow-[#1a2238]">
              <h3 className="text-lg font-semibold mb-4">Prochains Matchs</h3>
              <ul className="text-sm opacity-90">
                {selectedLeague ? leagues[selectedLeague].map((match, index) => (
                  <li key={index} className="py-1 cursor-pointer" onClick={() => setSelectedMatch(match)}>
                    {match}
                  </li>
                )) : "Sélectionnez une ligue pour voir les matchs"}
              </ul>
            </div>
            
            {/* Capabilities Card - Bet Types */}
            <div className="bg-gradient-to-br from-[#2B3257] to-[#344267] p-8 rounded-xl border border-[#4F5D84] shadow-lg shadow-[#1a2238]">
              <h3 className="text-lg font-semibold mb-4">Types de Paris</h3>
              {selectedMatch ? (
                <ul className="text-sm opacity-90">
                  {betTypes.map((bet, index) => (
                    <li key={index} className={`py-1 cursor-pointer ${selectedBetType === bet ? 'text-blue-400 font-semibold' : ''}`} onClick={() => setSelectedBetType(bet)}>
                      {bet}
                    </li>
                  ))}
                </ul>
              ) : "Sélectionnez un match pour voir les options de paris"}
            </div>
            
            {/* Limitations Card - Risk Levels */}
            <div className="bg-gradient-to-br from-[#2B3257] to-[#344267] p-8 rounded-xl border border-[#4F5D84] shadow-lg shadow-[#1a2238]">
              <h3 className="text-lg font-semibold mb-4">Risques des Paris</h3>
              <ul className="text-sm opacity-90">
                <li className="text-red-500">Très risqué</li>
                <li className="text-orange-500">Moyennement risqué</li>
                <li className="text-yellow-500">Risqué</li>
                <li className="text-green-500">Peu risqué</li>
              </ul>
            </div>
          </div>
          
          <div className="w-full max-w-3xl mt-16">
            <div className="flex flex-col md:flex-row items-center justify-center">
              <input type="text" placeholder="Entrez une question ici..." className="flex-1 px-4 py-3 rounded-md bg-white text-black w-full md:w-auto border border-[#4F5D84]" />
              <button className="ml-0 md:ml-4 mt-2 md:mt-0 px-6 py-3 rounded-md w-full md:w-auto bg-[#7440F4] border border-[#4F5D84]">Envoyer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}





