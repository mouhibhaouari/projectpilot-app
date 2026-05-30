import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', {
  state: () => ({
    selectedFolder: null,   
    analysisResult: null as any,
    lastError: null as any,
    projectStatus: 'idle',
  }),
  actions: {
    setSelectedFolder(folder: any) {
      this.selectedFolder = folder
    },
    setAnalysisResult(result: any) {
      this.analysisResult = result
      this.lastError = null
    },
    setError(error: any) {
      this.lastError = error
      this.analysisResult = null
      this.projectStatus = 'error';
    },
    setStatus(status: any) {
      this.projectStatus = status;
    }
  },
})