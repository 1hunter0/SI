import defaultSettings from '@/settings'

const title = defaultSettings.title || '中债威胁情报中心'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
