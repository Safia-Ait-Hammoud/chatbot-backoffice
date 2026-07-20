
import React from 'react'

// Pages principales
const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))
const projects = React.lazy(() => import('./views/projects/ProjectManagement'))
const Faq = React.lazy(() => import('./views/faq/Faq'))

/**
 * Array of route configuration objects
 *
 * @type {Array<Object>}
 * @property {string} path - URL path pattern
 * @property {string} name - Display name for breadcrumbs and navigation
 * @property {React.LazyExoticComponent} element - Lazy-loaded component
 * @property {boolean} [exact] - Whether to match path exactly
 *
 * @example
 * // Route renders when URL matches '/dashboard'
 * { path: '/dashboard', name: 'Dashboard', element: Dashboard }
 */
export const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/documentation', name: 'Documentation', element: projects },
  { path: '/faq', name: 'FAQ', element: Faq },
]

export default routes
