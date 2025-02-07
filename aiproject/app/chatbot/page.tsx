"use client";

import Head from "next/head";
import { ChevronDownIcon, ClockIcon, PlusCircleIcon, TrophyIcon, FlagIcon, ChartPieIcon, LockClosedIcon } from '@heroicons/react/24/outline';
import { useState, useEffect, useRef } from 'react';
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import axios from 'axios';

export default function Home() {
  const [isFootballOpen, setIsFootballOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [selectedBetType, setSelectedBetType] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const [messages, setMessages] = useState([
    { sender: "bot", text: "Bienvenue sur Bêt ! Posez-moi vos questions sur les paris sportifs." }
  ]);

  const [inputMessage, setInputMessage] = useState("")
  
  const chatContainerRef = useRef(null);
  

  const sendMessage = async () => {
    if (inputMessage.trim() === "" || inputMessage.length > 250) return;
    setMessages([...messages, { sender: "user", text: inputMessage }]);
    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        query: inputMessage,
        league: selectedLeague || "Ligue 1",
        // Vous pouvez compléter le payload si vous souhaitez passer team1, team2, bet, etc.
        team1: "",
        team2: "",
        bet: "draw"
      }, {
        headers: { "Content-Type": "application/json" }
      });
      const data = response.data;
      setMessages((prev) => [...prev, { sender: "bot", text: data.ai_response }]);
    } catch (error) {
      console.error("Erreur lors de l'envoi de la requête:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Une erreur s'est produite lors de la récupération de la réponse." }
      ]);
    }
    setInputMessage("");
  };









  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    console.log("Fetching matches...");
    Object.keys(leagues).forEach(league => {
      fetchLeagues(league);
    });
  }, []);
  

  const selectLeague = (league) => {
    setSelectedLeague(league);
    setMessages([...messages, { sender: "user", text: league }, { sender: "bot", text: "Choisissez un match ou posez votre pronostique." }]);
  };
  
  const selectMatch = (match) => {
    setSelectedMatch(match);
    setMessages(prevMessages => [
      ...prevMessages,
      { sender: "user", text: `Match sélectionné: ${match.teams} (${match.date} - ${match.time})` },
      { sender: "bot", text: "Sélectionnez un type de pari ou posez votre pronostique." }
    ]);
  };

  const selectBetType = (bet) => {
    setSelectedBetType(bet);
    setMessages(prevMessages => [...prevMessages, { sender: "user", text: `Type de pari sélectionné: ${bet.name}` }, { sender: "bot", text: "Pari sélectionné ! Vous pouvez maintenant analyser vos choix ou poser une question." }]);
  };

  

  const startNewChat = () => {
    setMessages([{ sender: "bot", text: "Bienvenue sur Bêt ! Posez-moi vos questions sur les paris sportifs." }]);
    setSelectedLeague(null);
    setSelectedMatch(null);
    setSelectedBetType(null);
    setInputMessage(""); // Réinitialise la barre de saisie
  };


  const sports = [
    { name: "Football", clickable: true },
    { name: "Tennis", clickable: false },
    { name: "Rugby", clickable: false },
    { name: "Basketball", clickable: false },
    { name: "Formule 1", clickable: false }
  ];

  const [leagues, setLeagues] = useState({
    "Premier League": [],
    "La Liga": [],
    "Serie A": [],
    "Bundesliga": [],
    "Ligue 1": []
  });
  
  useEffect(() => {
    console.log("Fetching matches...");
    const leagueNames = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"];
    leagueNames.forEach(league => {
      fetchLeagues(league);
    });
  }, []);
  

  useEffect(() => {
    console.log("Leagues updated:", leagues);
  }, [leagues]);
  

  function fetchLeagues(league) {
    console.log('Fetching matches for:', league);
  
    axios.post('http://127.0.0.1:5001/upcoming_matches', {
      league: league.replace(/\s+/g, "_") // Transforme "Premier League" en "Premier_League"
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    }).then((response) => {
      console.log('Response:', response.data); // Vérifie ce que l'API renvoie
  
      if (response.data && Array.isArray(response.data)) {
        setLeagues(prevLeagues => ({
          ...prevLeagues,
          [league]: response.data.map(match => ({
            teams: `${match.home_team} vs ${match.away_team}`,
            date: match.date,
            time: "Heure inconnue" // Si `time` est inexistant, tu peux changer cela selon ton API
          }))
        }));
      } else {
        console.error('Invalid response format:', response.data);
      }
    }).catch((error) => {
      console.error('Error fetching leagues:', error);
    });
  }
  

  const betTypes = [
    { name: "Résultat du match", icon: <TrophyIcon className="w-5 h-5" /> },
    { name: "Nombre de buts", icon: <ChartPieIcon className="w-5 h-5" /> },
    { name: "Équipe qui marque en premier", icon: <FlagIcon className="w-5 h-5" /> }
  ];

  const riskLevels = [
    { name: "Coup de poker", color: "text-red-500", image: "/Coup de poker.png" },
    { name: "Audacieux", color: "text-orange-500", image: "/audacieux.png" },
    { name: "Modéré", color: "text-yellow-500", image: "/Modéré.png" },
    { name: "Peu risqué", color: "text-green-500", image: "/peu risqué.png" }
  ];

  const navigation = [
    { name: 'Notre produit', href: '.#section' },
    { name: 'Tuto', href: '.#tuto' },
  ]
  useEffect(() => {
    // Appel API pour chaque ligue lors du montage du composant
    Object.keys(leagues).forEach(league => {
      fetchLeagues(league);
    });
  }, []);

  function fetchLeagues(league) {
    console.log('Fetching matches for:', league);
  
    axios.post('http://127.0.0.1:5001/upcoming_matches', {
      league: league.replace(/\s+/g, "_") // Envoie la league sans modification
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    }).then((response) => {
      console.log(`Response for ${league}:`, response.data); // Vérifie ce que l'API renvoie
  
      if (response.data && Array.isArray(response.data)) {
        setLeagues(prevLeagues => ({
          ...prevLeagues,
          [league]: response.data.map(match => ({
            teams: `${match.home_team} vs ${match.away_team}`, // Format propre
            date: match.date || "Date inconnue", // Gère les valeurs manquantes
            time: match.time || "Heure inconnue" // Gère les valeurs manquantes
          }))
        }));
      } else {
        console.error('Invalid response format for:', league, response.data);
      }
    }).catch((error) => {
      console.error('Error fetching matches for:', league, error);
    });
  }
  


  return (
    <div className="bg-gradient-to-br from-[#150931] to-[#344267] min-h-screen flex flex-col">
      <header className="absolute inset-x-0 top-0 z-50">
        <nav aria-label="Global" className="flex items-center justify-between p-6 lg:px-8">
        <button className="lg:hidden" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
          {isSidebarOpen ? <XMarkIcon className="w-6 h-6" /> : <Bars3Icon className="w-6 h-6" />}
        </button>
          <div className="flex lg:flex-1">
            <a href="." className="-m-1.5 p-1.5">
              <span className="sr-only">Your Company</span>
              <img
                alt=""
                src="/bet logo.png"
                className="h-8 w-auto"
              />
            </a>
            
          </div>
          
          <div className="flex lg:hidden">
            
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-white"
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon aria-hidden="true" className="size-6" />
            </button>
          </div>
          
          <div className="hidden lg:flex lg:flex-1 items-center lg:justify-end gap-12">
            <div className="hidden lg:flex lg:gap-x-12">
              {navigation.map((item) => (
                <a key={item.name} href={item.href} className="text-sm/6 font-semibold text-white">
                  {item.name}
                </a>
              ))}
            </div>
            <a href="/login" className="rounded-full bg-claire py-2.5 text-sm font-semibold text-white px-5 hover:bg-purple-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              Connexion 
            </a>
          </div>
        </nav>
        <Dialog open={mobileMenuOpen} onClose={setMobileMenuOpen} className="lg:hidden">
          <div className="fixed inset-0 z-50" />
          <DialogPanel className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-foncé px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div className="flex items-center justify-between">
              <a href="#" className="-m-1.5 p-1.5">
                <span className="sr-only">Your Company</span>
                <img
                  alt=""
                  src="/bet logo.png"
                  className="h-8 w-auto"
                />
              </a>
              <button
                type="button"
                onClick={() => setMobileMenuOpen(false)}
                className="-m-2.5 rounded-md p-2.5 text-white"
              >
                <span className="sr-only">Close menu</span>
                <XMarkIcon aria-hidden="true" className="size-6" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {navigation.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      className="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-white hover:bg-foncé"
                    >
                      {item.name}
                    </a>
                  ))}
                </div>
                <div className="py-6">
                  <a
                    href="/login"
                    className="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-white hover:bg-foncé"
                  >
                    Connexion
                  </a>
                </div>
              </div>
            </div>
          </DialogPanel>
        </Dialog>
      </header>

      <div className="flex flex-row h-screen">
        {/* Sidebar */}
        <div className={`fixed lg:relative top-0 left-0 w-64 bg-[#2B3257] p-6 text-white flex flex-col transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 transition-transform duration-300 ease-in-out`}>
        
            <nav className="mb-10 ">
              <h2 className="text-lg font-semibold mt-24">Sports</h2>
              
              <ul className="mt-3 space-y-4">
                <li className="py-2 cursor-pointer flex items-center justify-between" onClick={() => setIsFootballOpen(!isFootballOpen)}>
                  Football <ChevronDownIcon className={`w-5 h-5 inline transition-transform ${isFootballOpen ? 'rotate-180' : ''}`} />
                </li>
                {isFootballOpen && (
                  <ul className="ml-4 mt-2 opacity-90">
                    {Object.keys(leagues).map((league) => (
                      <li key={league} className={`py-1 cursor-pointer ${selectedLeague === league ? 'font-bold' : ''}`}onClick={() => selectLeague(league)}>
                        {league}
                      </li>
                    ))}
                  </ul>
                )}
                 
              <li className="flex items-center justify-between p-2 rounded-md opacity-50"> 
                Tennis <LockClosedIcon className="w-5 h-5 text-gray-400" />
              </li>
              <li className="flex items-center justify-between p-2 rounded-md opacity-50"> 
                Rugby <LockClosedIcon className="w-5 h-5 text-gray-400" />
              </li>
              <li className="flex items-center justify-between p-2 rounded-md opacity-50"> 
                Basketball <LockClosedIcon className="w-5 h-5 text-gray-400" />
              </li>
              <li className="flex items-center justify-between p-2 rounded-md opacity-50"> 
                Formule 1 <LockClosedIcon className="w-5 h-5 text-gray-400" />
              </li>
              </ul>
            </nav>
            
          <button className="mt-auto bg-[#7440F4] flex items-center justify-center px-6 py-3 rounded-md text-lg" onClick={startNewChat}>
          <PlusCircleIcon className="w-6 h-6 mr-2" /> Nouveau Chat
          </button>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-25 pb-10 text-white flex flex-col items-center justify-between">
        <div className={`text-center mt-[90px] transition-opacity duration-300 ${isSidebarOpen ? 'opacity-0' : 'opacity-100'}`}>
        <p className="mb-5 opacity-80 text-lg">Les paris peuvent être addictifs et sont interdit au moins de 18 ans.<br></br> Pariez de manière responsable et respectez la législation locale. </p>
          </div>
          
          <div className="hidden sm:grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl pb-5">
            {/* Example Card - Matches */}
            <div className="chat-container bg-gradient-to-br from-[#2B3257] to-[#344267] p-6 rounded-xl border border-[#4F5D84] shadow-lg shadow-[#1a2238] w-full h-80 overflow-y-auto">
              <h3 className="text-lg font-semibold mb-4 text-center ">Prochains matchs</h3>
              <div className="flex flex-col gap-4">
              {selectedLeague && leagues[selectedLeague]?.length > 0 ? (
                leagues[selectedLeague].map((match, index) => (
                  <div key={index} className="p-4 bg-[#344267] rounded-lg shadow-md cursor-pointer hover:bg-[#3a4b6c] flex flex-col" onClick={() => selectMatch(match)}>
                    <h4 className="text-md font-semibold">{match.teams}</h4>
                    <p className="text-sm opacity-80">{match.date} - {match.time}</p>
                  </div>
                ))
              ) : (
                <p className="text-center text-sm opacity-80">Aucun match disponible</p>
              )}

              </div>
            </div>
            
            {/* Capabilities Card - Bet Types */}
            <div className="bg-gradient-to-br h-80 from-[#2B3257] to-[#344267] p-6 rounded-xl border border-[#4F5D84] shadow-lg shadow-[#1a2238]">
              <h3 className="text-lg text-center font-semibold mb-4">Types de paris</h3>
              {selectedMatch ? (
                <div className="flex flex-col gap-4">
                  {betTypes.map((bet, index) => (
                    <button key={index} className="flex items-center gap-3 p-4 bg-[#3a4b6c] rounded-lg shadow-md hover:bg-[#4b5e7d] text-left" onClick={() => selectBetType(bet)}>
                      {bet.icon}
                      <span>{bet.name}</span>
                    </button>
                  ))}
                </div>
              ) : "Sélectionnez un match pour voir les options de paris"}
            </div>

            
             {/* Limitations Card - Risk Levels (Ordered) */}
             <div className="bg-gradient-to-br from-[#2B3257] to-[#344267] p-6 rounded-xl border border-[#4F5D84] h-80 shadow-lg w-full">
              <h3 className="text-lg font-semibold mb-4 text-center">Courbe de risques</h3>
              <div className="grid grid-cols-1 gap-2">
                {riskLevels.map((risk, index) => (
                  <div key={index} className="flex items-center p-1 transition-transform transform">
                    <img src={risk.image} alt={risk.name} className="w-10 h-10 mr-4" />
                    <span className={`text-lg font-medium ${risk.color}`}>{risk.name}</span>
                  </div>
                ))}
              </div>
            </div>
            </div>


           {/* Chat Section */}
           <div className="chat-container w-full max-w-5xl h-96 overflow-y-auto  p-4 rounded-md" ref={chatContainerRef}>
           {messages.map((msg, index) => (
              <div key={index} className={`my-2 p-3 rounded-md ${msg.sender === "user" ? "bg-claire text-right ml-auto" : "bg-gray-700 text-left mr-auto"} w-fit max-w-[80%]`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="text-sm opacity-80 mb-4">Messages: {messages.length}</div>


          
          {/* Input Section */}
          <div className="w-full max-w-3xl mt-4 px-4 sm:px-0">
            {inputMessage.length > 250 && <div className="text-red-500 text-left text-sm">Votre message ne doit pas dépasser 250 caractères.</div>}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <input 
                type="text" 
                placeholder="Entrez une question ici..." 
                className="flex-1 px-4 py-3 rounded-md bg-white text-black w-full sm:w-auto border border-[#4F5D84]" 
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              />
              <button 
                className="px-6 py-3 rounded-md w-full sm:w-auto bg-[#7440F4] border border-[#4F5D84]"
                onClick={sendMessage}
              >
                Envoyer
              </button>
            </div>
            <div className="text-right text-sm opacity-80 mt-2">{inputMessage.length} / 250 caractères</div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white dark:bg-[#150931] w-full py-6 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div className="max-w-screen-xl mx-auto flex flex-col sm:flex-row justify-between">
          <div className="mb-6 sm:mb-0">
            <a href="" className="flex items-center">
              <img src="/bet logo.png" className="h-20 me-3" alt="FlowBite Logo" />
            </a>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            <div>
              <h2 className="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Nos réseaux</h2>
              <ul className="text-gray-500 dark:text-gray-400 font-medium">
                <li className="mb-4"><a href="https://github.com/pierrrebouillard/IA_BOT" className="hover:underline">Github</a></li>
                <li><a href="https://clickup.com" className="hover:underline">ClickUp</a></li>
              </ul>
            </div>
            <div>
              <h2 className="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Legal</h2>
              <ul className="text-gray-500 dark:text-gray-400 font-medium">
              <li className="mb-4"><a href="mentions_legales" className="hover:underline">Mentions légales</a></li>
              <li className="mb-4"><a href="politique_de_confidentialite" className="hover:underline">Politique de Confidentialité</a></li>
              <li className="mb-4"><a href="CGU" className="hover:underline">Conditions générales d'utilisation</a></li>
              <li className="mb-4"><a href="politique_de_cookies" className="hover:underline">Politique des cookies</a></li>
              <li><a href="securite_des_donnees" className="hover:underline">Sécurité et utilisation responsable</a></li>
              </ul>
            </div>
          </div>
        </div>
        <hr className="my-6 border-gray-200 dark:border-gray-700" />
        <div className="text-center text-sm text-gray-500 dark:text-gray-400">© 2025 <a href="https://Bêt.com/" className="hover:underline">Bêt™</a>. All Rights Reserved.</div>
      </footer>
    </div>


  );
}
