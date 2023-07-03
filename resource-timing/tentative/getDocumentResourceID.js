function getDocumentResourceID() {
    return new Promise(resolve => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntriesByType('navigation');
        if (entries.length > 0) {
          observer.disconnect();
          const [entry] = entries;
          const { name, startTime } = entry;
          resolve(`${name}/${startTime}`);
        }
      });
      observer.observe({entryTypes: ['navigation']});
    });
}
