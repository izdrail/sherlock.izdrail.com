
import axios from 'axios';


class ResultsManager {
    private searchTerm: any;
    private totalResults: number;
    private totalPages: number;
    private currentPage: number;
    private results: any[];

    constructor() {
        this.results = [];
        this.currentPage = 1;
        this.totalPages = 1;
        this.totalResults = 0;
        this.searchTerm = '';
    }

    async getResults(searchTerm, page) {
        this.searchTerm = searchTerm;
        this.currentPage = page;

        const response = await axios.get(`/api/search?q=${searchTerm}&page=${page}`);

        this.results = response.data.results;
        this.totalPages = response.data.total_pages;
        this.totalResults = response.data.total_results;
    }

    getResultsByPage(page) {
        return this.results.slice((page - 1) * 10, page * 10);
    }

    getCurrentPage() {
        return this.currentPage;
    }

    getTotalPages() {
        return this.totalPages;
    }

    getTotalResults() {
        return this.totalResults;
    }

    getSearchTerm() {
        return this.searchTerm;
    }
}

export default ResultsManager;