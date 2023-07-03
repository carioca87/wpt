function getResourceID(resourceName) {
    return new Promise(resolve => {
      const observer = new PerformanceObserver(list => {
        const entries = list.getEntriesByType('resource');
        for (const entry of entries) {
          if (entry.name.endsWith(resourceName)) {
            observer.disconnect();name
            resolve(`${entry.name}/${entry.startTime}`);
            return;
          }
        }
      });
      observer.observe({entryTypes: ['resource']});
    });
}
