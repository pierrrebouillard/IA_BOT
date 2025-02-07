"use client";


import Link from "next/link";
import { useState } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { SparklesIcon, StarIcon, EyeIcon, PaintBrushIcon, ClockIcon, HandThumbUpIcon } from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Chatbot', href: '/chatbot' },
  { name: 'Notre produit', href: '#section' },
  { name: 'Tuto', href: '#tuto' },
 
]
const features = [
  {
    name: 'Analyses en temps réel',
    description:
      'Consultez des statistiques fiables sur les équipes et joueurs. Tout est conçu pour éclairer vos décisions.',
    icon: ClockIcon
  ,
  },
  {
    name: 'Prédictions IA avancées',
    description:
      "Profitez d'algorithmes d'apprentissage automatique pour des pronostics optimisés.",
    icon: EyeIcon,
  },
  {
    name: 'Une expérience sur mesure',
    description:
      'Bêt ajuste ses analyses à votre profil. Des conseils personnalisés pour maximiser vos chances.',
    icon: PaintBrushIcon,
  },
  {
    name: 'Simplicité et efficacité security',
    description:
      'Focalisez-vous sur vos choix, Bêt gère les détails. On vous simplifie vraiment la vie.',
    icon: SparklesIcon,
  },
  {
    name: 'Accompagnement constant',
    description:
      'Notre chatbot réactif est toujours prêt à vous aider. Vous pouvez compter sur nous à chaque étape.',
    icon: HandThumbUpIcon,
  },
  {
    name: 'Chatbot expert 24/7',
    description:
      ' Posez vos questions à Bêt, votre assistant IA, et obtenez des réponses instantanées !',
    icon: StarIcon,
  },
]

export default function Example() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="bg-violet">

    <div className="bg-violet">
      <header className="absolute inset-x-0 top-0 z-50">
        <nav aria-label="Global" className="flex items-center justify-between p-6 lg:px-8">
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

      <div className="relative isolate px-6 pt-14 lg:px-10">
        <div
          aria-hidden="true"
          className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
        >
         
        </div>
        <div className="mx-auto max-w-2xl pt-12 pb-32 sm:py-20 lg:py-20">
  
        <div className="max-w-4xl w-full bg-violet p-8 rounded-lg shadow-lg border border-violet">
        <h1 className="text-3xl font-bold text-center mb-6">Sécurité et Utilisation Responsable</h1>
        <p className="text-sm opacity-80 text-center mb-8">Dernière mise à jour : 07/02/2025</p>

        <div className="space-y-6 text-gray-300 text-sm md:text-base">
        <section>
            <h2 className="text-lg font-semibold text-white">1. Sécurité des données</h2>
            <p>L’équipe de Bêt met tout en œuvre pour assurer la protection des données des utilisateurs. Cependant, certaines mesures de sécurité ne sont pas encore en place, notamment le chiffrement des mots de passe et les protections avancées contre les attaques.</p>
            <p>Nous encourageons les utilisateurs à rester vigilants et à éviter de partager leurs informations sensibles.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">2. Bonnes pratiques pour l’utilisation du service</h2>
            <p>Bien que notre chatbot fournisse des conseils, les utilisateurs doivent exercer leur propre jugement lors de la prise de décisions de paris sportifs.</p>
            <ul className="list-disc ml-6">
              <li>Utiliser le service de manière responsable et comprendre ses limites.</li>
              <li>Ne pas considérer les recommandations comme des garanties de gains.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">3. Responsabilité en cas de faille de sécurité</h2>
            <p>Bêt ne garantit pas une sécurité absolue contre les attaques. En cas de faille, nous nous engageons à :</p>
            <ul className="list-disc ml-6">
              <li>Corriger le problème dans les meilleurs délais.</li>
              <li>Informer les utilisateurs concernés si leurs données sont compromises.</li>
            </ul>
            <p>Toutefois, Bêt ne pourra être tenu responsable d’une fuite de données indépendante de notre volonté.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">4. Utilisation responsable du chatbot et interdictions</h2>
            <p>Il est interdit d’utiliser Bêt pour :</p>
            <ul className="list-disc ml-6">
              <li>Manipuler des paris ou contourner des réglementations.</li>
              <li>Employer des bots ou scripts automatisés.</li>
              <li>Tenter d’accéder illégalement au service ou d’en exploiter les failles.</li>
            </ul>
            <p>Tout non-respect de ces règles entraînera des sanctions.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">5. Sanctions en cas de non-respect</h2>
            <p>En cas de violation des règles de sécurité, Bêt peut appliquer :</p>
            <ul className="list-disc ml-6">
              <li>Blocage immédiat de l’accès au service.</li>
              <li>Bannissement définitif du compte utilisateur.</li>
              <li>Blocage de l’adresse IP.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">6. Utilisation des données scrapées de FBRef</h2>
            <p>Bêt analyse des données publiques issues de FBRef tout en respectant leurs restrictions.</p>
            <p>Nous collectons uniquement les données autorisées :</p>
            <ul className="list-disc ml-6">
              <li>Compétitions : <a href="https://fbref.com/en/comps/" className="text-blue-400 underline">https://fbref.com/en/comps/</a></li>
              <li>Matchs et statistiques : <a href="https://fbref.com/en/matches/" className="text-blue-400 underline">https://fbref.com/en/matches/</a></li>
            </ul>
            <p>Si FBRef modifie ses règles, nous ajusterons immédiatement notre politique.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">7. Mise à jour de cette politique</h2>
            <p>Cette politique peut être mise à jour en fonction des évolutions technologiques et légales. Nous recommandons aux utilisateurs de la consulter régulièrement.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-white">8. Contact</h2>
            <p>Pour toute question relative à la sécurité du service, contactez :</p>
            <p>📩 <span className="text-blue-400">Jules Toublant</span> - <a href="mailto:jules.toublant@epitech.digital" className="underline">jules.toublant@epitech.digital</a></p>
          </section>
        </div>



            
            
          </div>
        </div>
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
        >
          
         
        </div>
      </div>

















        <div className="bg-white dark:bg-violet" >
          <div className="mx-auto w-full max-w-screen-xl p-4 pt-64 pb-9 ">
            <div className="md:flex md:justify-between">
                <div className="mb-6 md:mb-0">
                  <a href="" className="flex items-center">
                  <img src="/bet logo.png" className="h-20 me-3" alt="FlowBite Logo" />
              </a>
          </div>
          <div className="grid grid-cols-2 gap-8 sm:gap-6 justify-end sm:grid-cols-2">
              
              <div>
                  <h2 className="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white">Nos réseaux</h2>
                  <ul className="text-gray-500 dark:text-gray-400 font-medium">
                      <li className="mb-4">
                          <a href="https://github.com/pierrrebouillard/IA_BOT" className="hover:underline ">Github</a>
                      </li>
                      <li>
                          <a href="https://clickup.com" className="hover:underline">ClickUp</a>
                      </li>
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
      <hr className="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
      <div className="sm:flex sm:items-center sm:justify-center">
          <span className="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2025 <a href="https://Bêt.com/" className="hover:underline">Bêt™</a>. All Rights Reserved.
          </span>
          <div className="flex mt-4 sm:justify-center sm:mt-0">
          </div>
        </div>
      </div>
    </div>

    </div>
    
    </div>

    
  
  )
}