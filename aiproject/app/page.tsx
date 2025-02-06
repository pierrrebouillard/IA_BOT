'use client'
import Link from "next/link";
import { useState } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { SparklesIcon, StarIcon, EyeIcon, PaintBrushIcon, ClockIcon, HandThumbUpIcon } from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Chatbot', href: '#' },
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
            <a href="#" className="-m-1.5 p-1.5">
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
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
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
              Connexion <span aria-hidden="true">&rarr;</span>
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
                className="-m-2.5 rounded-md p-2.5 text-gray-700"
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
                      className="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-white hover:bg-gray-50"
                    >
                      {item.name}
                    </a>
                  ))}
                </div>
                <div className="py-6">
                  <a
                    href="/login"
                    className="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-white hover:bg-gray-50"
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
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-[calc(50%-11rem)] aspect-1155/678 w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-linear-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
          />
        </div>
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-64">
  
          <div className="text-center">
            <h2 className="text-5xl font-semibold tracking-tight text-balance text-white sm:text-6xl">
            Analyse sportive sans prise de tête, gagnez <br></br>plus avec l'IA !
            </h2>
            <p className="mt-8 text-lg font-medium text-pretty text-gray-500 sm:text-l/8">
            Bêt, l'assistant IA qui vous aide à prendre les meilleures décisions, que vous soyez un parieur prudent ou un amateur de paris audacieux. Simplifiez vos choix, profitez des statistiques fiables !
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <a
                href="#"
                className="rounded-full bg-white py-2.5 text-sm font-semibold text-violet px-8 hover:bg-stone-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Essayer Bêt
              </a>
              <a
                href="#section"
                className="rounded-full bg-violet py-2.5 text-sm font-semibold text-white shadow-xs px-8 border border-white hover:bg-stone-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                En savoir plus
              </a>
              {/* <a href="#" className="text-sm/6 font-semibold text-gray-900">
                Learn more <span aria-hidden="true">→</span>
              </a> */}
            </div>
          </div>
        </div>
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-[calc(50%+3rem)] aspect-1155/678 w-[36.125rem] -translate-x-1/2 bg-linear-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
          />
         
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-purple-900/30 to-transparent" />




      <div id="section" className="bg-violet py-24 sm:py-64">
      <div className="mx-auto max-w-7xl px-6 lg:px-8 pt-20">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base/7 font-semibold text-claire">Parier plus vite</h2>
          <p className="mt-2 text-4xl font-semibold tracking-tight text-pretty text-white sm:text-5xl lg:text-balance">
          Ce que Bêt fait pour vous
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-6xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-11 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
            {features.map((feature) => (
              <div key={feature.name} className="relative pl-16">
                <dt className="text-base/7 font-semibold text-white">
                  <div className="absolute top-0 left-0 flex size-10 items-center justify-center rounded-lg bg-claire">
                    <feature.icon aria-hidden="true" className="size-6 text-white" />
                  </div>
                  {feature.name}
                </dt>
                <dd className="mt-2 text-base/7 text-white">{feature.description}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>




    <div className="bg-violet">
      <div className="mx-auto max-w-7xl py-24 sm:py-64 sm:px-6 lg:px-8">
        <div className="relative isolate overflow-hidden justify-center bg-foncé px-6 pt-16 shadow-2xl sm:rounded-3xl sm:px-16 md:pt-24 lg:flex lg:px-24 lg:pt-0">
          <svg
            viewBox="0 0 1024 1024"
            aria-hidden="true"
            className="absolute top-1/2 left-1/2 -z-10 size-[64rem] -translate-y-1/2 [mask-image:radial-gradient(closest-side,white,transparent)] sm:left-full sm:-ml-80 lg:left-1/2 lg:ml-0 lg:-translate-x-1/2 lg:translate-y-0"
          >
            <circle r={512} cx={512} cy={512} fill="url(#759c1415-0410-454c-8f7c-9a820de03641)" fillOpacity="0.7" />
            <defs>
              <radialGradient id="759c1415-0410-454c-8f7c-9a820de03641">
                <stop stopColor="#7440F4" />
                <stop offset={1} stopColor="#7440F4" />
              </radialGradient>
            </defs>
          </svg>
          <div className="mx-auto max-w-md text-center items-center justify-center lg:mx-0 lg:flex-auto lg:py-32 lg:text-left">
            <h2 className="text-3xl font-semibold text-center tracking-tight text-balance text-white sm:text-3xl">
            Gagnez en précision. Gagnez en confiance, et parier plus intelligemment grâce à l’IA !          
            </h2>
            
            <div className="mt-10 flex text-center items-center gap-x-6 justify-center">
              <a
                href="login"
                className="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold  text-gray-900 shadow-xs hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Créer un compte
              </a>
             
            </div>
          </div>
          <div className="relative mt-28 lg:mt-8">
            
          </div>
        </div>
      </div>
    </div>
















    <div className="bg-violet">
      <div id ="tuto" className="mx-auto max-w-7xl py-24 sm:px-6 sm:py-64 lg:px-8">
      <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="mt-2 text-4xl font-semibold tracking-tight text-center text-pretty text-white sm:text-5xl lg:text-balance">
          Découvrez Bêt en action !
          </h2>
          <p className="mt-8 text-lg font-medium text-pretty text-center sm:pb-14 text-gray-500 sm:text-l/8">
          Regardez comment Bêt vous aide à analyser, prédire et gagner grâce à l'IA. En moins de 2 minutes, vous apprendrez comment utiliser notre IA pour optimiser vos paris, comment lire nos prédictions et notre échelle de risque et comment suivre vos performances et maximiser vos gains. Regardez maintenant et passez au niveau supérieur !            </p>
        </div>
        <div className="relative isolate overflow-hidden justify-center bg-foncé px-6 pt-16 shadow-2xl sm:rounded-3xl sm:px-16 md:pt-24 lg:flex lg:px-24 lg:pt-0">
          <svg
            viewBox="0 0 1024 1024"
            aria-hidden="true"
            className="absolute top-1/2 left-1/2 -z-10 size-[64rem] -translate-y-1/2 [mask-image:radial-gradient(closest-side,white,transparent)] sm:left-full sm:-ml-80 lg:left-1/2 lg:ml-0 lg:-translate-x-1/2 lg:translate-y-0"
          >
            <circle r={512} cx={512} cy={512} fill="url(#759c1415-0410-454c-8f7c-9a820de03641)" fillOpacity="0.7" />
            <defs>
              <radialGradient id="759c1415-0410-454c-8f7c-9a820de03641">
                <stop stopColor="#7440F4" />
                <stop offset={1} stopColor="#7440F4" />
              </radialGradient>
            </defs>
          </svg>
          <div className="mx-auto max-w-md text-center items-center justify-center lg:mx-0 lg:flex-auto lg:py-32 lg:text-left">
            
          </div>
          <div className="relative mt-28 lg:mt-8">
            
          </div>
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
                      <li className="mb-4">
                          <a href="#" className="hover:underline">Confidentialité</a>
                      </li>
                      <li>
                          <a href="#" className="hover:underline">Sécurité, utilisation<br></br> &amp; Conditions</a>
                      </li>
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

    
    </div>
  
  )
}

