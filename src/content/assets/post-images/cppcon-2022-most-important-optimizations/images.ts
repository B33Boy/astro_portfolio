const imageModules = import.meta.glob('./*.{png,jpg,jpeg,webp,avif}', {
    import: 'default',
    eager: true
  });
  
  // Convert to a cleaner export object (e.g., without "./" and extension in key)
  export const images: Record<string, unknown> = {};
  
  for (const path in imageModules) {
    const name = path.split('/').pop()?.split('.')[0] || '';
    images[name] = imageModules[path];
  }
  