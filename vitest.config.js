export default {
    test: {
        include: ['web/tests/**/*.js'],
        environment: 'jsdom',
        globals: true,
        coverage: {
            provider: 'v8',
            reporter: ['text', 'html'],
            include: ['web/static/js/**/*.js'],
            exclude: ['web/static/js/main.js'],
        },
    },
};
