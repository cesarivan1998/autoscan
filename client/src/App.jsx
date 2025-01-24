import {BrowserRouter, Routes, Route} from 'react-router-dom'
import { CarsPage } from './pages/CarsPage'
import { BrandsPage } from './pages/BrandsPage'
import { BrandFormPage } from './pages/BrandFormPage'
import { CarFormPage } from './pages/CarFormPage'
import { Navigation } from "./components/Navigation"

function App() {
  return (
    <BrowserRouter>
    <Navigation />
    <Routes>
      <Route path="/" element={<BrandsPage />}/>
      <Route path="/brands" element={<BrandsPage />}/>
      <Route path="/cars" element={<CarsPage />}/>
      <Route path="/brands-create" element={<BrandFormPage />}/>
      <Route path="/cars-create" element={<CarFormPage />}/>
    </Routes>
    </BrowserRouter>
  )
}

export default App