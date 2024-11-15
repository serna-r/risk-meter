function evaluatePassword() {
    const password = document.getElementById('password').value;
    const result = zxcvbn(password);

    // Update general password strength details
    document.getElementById('passwordField').textContent = password || 'N/A';
    document.getElementById('guesses').textContent = result.guesses;
    document.getElementById('guessesLog10').textContent = result.guesses_log10.toFixed(2);
    document.getElementById('onlineCrackTime').textContent = result.crack_times_display.online_throttling_100_per_hour;
    document.getElementById('offlineSlowCrackTime').textContent = result.crack_times_display.offline_slow_hashing_1e4_per_second;
    document.getElementById('offlineFastCrackTime').textContent = result.crack_times_display.offline_fast_hashing_1e10_per_second;
    document.getElementById('feedbackWarning').textContent = result.feedback.warning || 'None';
    document.getElementById('suggestions').textContent = result.feedback.suggestions.join(', ') || 'None';
    document.getElementById('passwordScore').textContent = result.score; // Add score display

    // Update password component analysis
    const componentAnalysis = document.getElementById('componentAnalysis');
    componentAnalysis.innerHTML = ''; // Clear previous entries

    result.sequence.forEach(component => {
        const row = document.createElement('tr');

        const patternCell = document.createElement('td');
        patternCell.textContent = component.pattern;

        const tokenCell = document.createElement('td');
        tokenCell.textContent = component.token;

        const detailsCell = document.createElement('td');
        if (component.pattern === 'spatial') {
            detailsCell.textContent = `Graph: ${component.graph}, Turns: ${component.turns}, Shifted Count: ${component.shifted_count}`;
        } else if (component.pattern === 'dictionary') {
            detailsCell.textContent = `Dictionary: ${component.dictionary_name}, Word: ${component.matched_word}, Rank: ${component.rank}`;
        } else {
            detailsCell.textContent = 'N/A';
        }

        const guessesCell = document.createElement('td');
        guessesCell.textContent = component.guesses;

        const logGuessesCell = document.createElement('td');
        logGuessesCell.textContent = component.guesses_log10.toFixed(2);

        // Append cells to the row
        row.appendChild(patternCell);
        row.appendChild(tokenCell);
        row.appendChild(detailsCell);
        row.appendChild(guessesCell);
        row.appendChild(logGuessesCell);

        // Append row to the table body
        componentAnalysis.appendChild(row);
    });
}
