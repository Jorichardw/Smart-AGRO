import React from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import {
  Home,
  Leaf,
  Cloud,
  Bot,
  BarChart3,
  ShoppingCart,
  Settings,
  HelpCircle,
  Users,
  MapPin,
  Droplets,
  Bug,
  TrendingUp,
  Calendar,
  Camera,
  MessageSquare
} from 'lucide-react'

const Sidebar = ({ isOpen, onClose, user }) => {
  const router = useRouter()

  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: Home,
      description: 'Overview and stats'
    },
    {
      name: 'My Farms',
      href: '/farms',
      icon: Leaf,
      description: 'Farm management'
    },
    {
      name: 'Crops',
      href: '/crops',
      icon: MapPin,
      description: 'Crop monitoring'
    },
    {
      name: 'Weather',
      href: '/weather',
      icon: Cloud,
      description: 'Weather & forecasts'
    }
  ]

  const aiTools = [
    {
      name: 'Disease Detection',
      href: '/ai/disease-detection',
      icon: Camera,
      description: 'AI disease analysis'
    },
    {
      name: 'Pest Detection',
      href: '/ai/pest-detection',
      icon: Bug,
      description: 'Pest identification'
    },
    {
      name: 'Crop Recommendations',
      href: '/ai/recommendations',
      icon: TrendingUp,
      description: 'AI crop suggestions'
    },
    {
      name: 'AI Assistant',
      href: '/ai/chat',
      icon: MessageSquare,
      description: 'Farming advisor'
    }
  ]

  const tools = [
    {
      name: 'Irrigation',
      href: '/irrigation',
      icon: Droplets,
      description: 'Water management'
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      description: 'Farm analytics'
    },
    {
      name: 'Marketplace',
      href: '/marketplace',
      icon: ShoppingCart,
      description: 'Buy & sell'
    },
    {
      name: 'Calendar',
      href: '/calendar',
      icon: Calendar,
      description: 'Farm planning'
    }
  ]

  const bottomLinks = [
    { name: 'Settings', href: '/settings', icon: Settings },
    { name: 'Help & Support', href: '/help', icon: HelpCircle }
  ]

  const NavItem = ({ item, isActive, onClick }) => {
    const Icon = item.icon
    
    return (
      <Link
        href={item.href}
        className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors ${
          isActive
            ? 'bg-green-100 text-green-900'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
        }`}
        onClick={onClick}
      >
        <Icon
          className={`mr-3 flex-shrink-0 h-5 w-5 transition-colors ${
            isActive ? 'text-green-500' : 'text-gray-400 group-hover:text-gray-500'
          }`}
        />
        <div className="flex-1">
          <span>{item.name}</span>
          {item.description && (
            <p className="text-xs text-gray-500 mt-0.5">{item.description}</p>
          )}
        </div>
      </Link>
    )
  }

  const NavSection = ({ title, items }) => (
    <div className="mb-6">
      <h3 className="px-2 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
        {title}
      </h3>
      <nav className="space-y-1">
        {items.map((item) => (
          <NavItem
            key={item.name}
            item={item}
            isActive={router.pathname === item.href || router.pathname.startsWith(item.href + '/')}
            onClick={() => isOpen && onClose && onClose()}
          />
        ))}
      </nav>
    </div>
  )

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* User Profile Section */}
      <div className="flex-shrink-0 px-4 py-6 border-b border-gray-200">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-10 w-10 bg-green-600 rounded-full flex items-center justify-center">
              <Users className="h-5 w-5 text-white" />
            </div>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">
              {user?.first_name} {user?.last_name}
            </p>
            <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <NavSection title="Main" items={navigation} />
        <NavSection title="AI Tools" items={aiTools} />
        <NavSection title="Tools" items={tools} />
      </div>

      {/* Bottom Links */}
      <div className="flex-shrink-0 border-t border-gray-200 px-4 py-4">
        <nav className="space-y-1">
          {bottomLinks.map((item) => (
            <NavItem
              key={item.name}
              item={item}
              isActive={router.pathname === item.href}
              onClick={() => isOpen && onClose && onClose()}
            />
          ))}
        </nav>
      </div>
    </div>
  )

  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden lg:flex lg:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 border-r border-gray-200 bg-white">
            {sidebarContent}
          </div>
        </div>
      </div>

      {/* Mobile Sidebar */}
      {isOpen && (
        <div className="fixed inset-0 flex z-40 lg:hidden">
          <div className="flex-shrink-0 w-14" aria-hidden="true">
            {/* Force sidebar to shrink to fit close icon */}
          </div>
          
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <div className="absolute top-0 right-0 -mr-12 pt-2">
              <button
                type="button"
                className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                onClick={onClose}
              >
                <span className="sr-only">Close sidebar</span>
                <X className="h-6 w-6 text-white" />
              </button>
            </div>
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  )
}

export default Sidebar