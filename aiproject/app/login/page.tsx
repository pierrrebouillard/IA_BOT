"use client";

import { useState } from "react";
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'


const navigation = [
  { name: 'Chatbot', href: '#' },
  { name: 'Notre produit', href: '.#section' },
  { name: 'Tuto', href: '.#tuto' },
]




export default function Register() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [id]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // #send to backend api {"username": "Prod_test", "password": "Test"} http://127.0.0.1:5000/register
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: formData.email,
        password: formData.password,
      }),
    });
    // check the response and redirect to the right page
  }

    return(
   <div className="bg-violet">
         <header className="absolute inset-x-0 top-0 z-50">
           <nav aria-label="Global" className="flex items-center justify-between p-6 lg:px-8">
             <div className="flex lg:flex-1">
               <a href=".#" className="-m-1.5 p-1.5">
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
                    
                   </div>
                 </div>
               </div>
             </DialogPanel>
           </Dialog>
         </header>
  







      <div className=" right-0 left-0 z-50 flex justify-center items-center w-full h-screen bg-violet bg-opacity-50">
          <div className="relative p-4 w-full max-w-md">
            {/* Contenu du Modal */}
            <div className="relative bg-white rounded-lg shadow-sm dark:bg-foncé">
              {/* Header du Modal */}
              <div className="flex items-center justify-center p-4 md:p-5 border-b rounded-t dark:border-gray-600 border-gray-200">
                <h3 className="text-xl font-semibold text-center text-gray-900 dark:text-white">
                  Connexion
                </h3>
              </div>
              {/* Body du Modal */}
              <div className="p-4 md:p-5">
                <form className="space-y-4" onSubmit={handleSubmit}>
                  <div>
                    <label
                      htmlFor="email"
                      className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                    >
                      Email
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-claire focus:border-claire block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                      placeholder="nom@adresse.com"
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div>
                    <label
                      htmlFor="password"
                      className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                    >
                      Mot de passe
                    </label>
                    <input
                      type="Mot de passe"
                      id="password"
                      placeholder="••••••••"
                      className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                      required
                      onChange={handleChange}
                    />
                  </div>
                  <div className="flex justify-between">
                  </div>
                  <button
                    type="submit"
                    className="w-full text-white bg-claire hover:bg-claire focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-claire dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  >
                    Connectez-vous à votre compte
                  </button>
                  <div className="text-sm font-medium text-gray-500 dark:text-gray-300">
                    Pas de compte ?{" "}
                    <a
                      href="/register"
                      className="text-claire hover:underline dark:text-claire"
                    >
                      Créer un compte
                    </a>
                  </div>
                </form>
              </div>
            </div>
          </div>
          </div>

          <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-purple-900/30 to-transparent" />

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

   


    )
  }
