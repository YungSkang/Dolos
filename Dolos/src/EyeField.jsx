import { useEffect, useRef } from 'react'

function EyeField({ count }) {
  const containerRef = useRef(null)

  useEffect(() => {
  const container = containerRef.current
  if (!container) return

  // Build a grid of cells — e.g. 4 cols × 3 rows = 12 slots
  const cols = 4
  const rows = Math.ceil(count / cols)

  let index = 0
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (index >= count) break

      const img = document.createElement('img')
      img.src = '/eye.png'
      img.setAttribute('aria-hidden', 'true')

      const size = 70 + Math.random() * 100        // 70px – 170px (smaller max)

      // Cell boundaries as percentages
      const cellW = 100 / cols
      const cellH = 100 / rows

      // Random position within the cell, with padding so edges don't clip
      const padding = 8
      const x = col * cellW + padding + Math.random() * (cellW - padding * 2)
      const y = row * cellH + padding + Math.random() * (cellH - padding * 2)

      const dur = 14 + Math.random() * 18
      const del = Math.random() * 20

      Object.assign(img.style, {
        position:      'absolute',
        width:         `${size}px`,
        height:        `${size}px`,
        left:          `${x}%`,
        top:           `${y}%`,
        opacity:       '0',
        mixBlendMode:  'screen',
        pointerEvents: 'none',
        animation:     `eyeWatch ${dur}s ease-in-out ${del}s infinite`,
        transform:     'translate(-50%, -50%)',
      })

      container.appendChild(img)
      index++
    }
  }

  return () => { container.innerHTML = '' }
}, [count])

  return (
    <div
      ref={containerRef}
      style={{
        position:      'fixed',
        inset:         0,
        zIndex:        0,
        pointerEvents: 'none',
        overflow:      'hidden',
      }}
    />
  )
}

export default EyeField