// JavaScript Code
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('keyword-button').addEventListener('click', function() {
        let keywordList = document.getElementById('keyword-list');
        keywordList.innerHTML = ''; // Clear the list first
        
        // Make a fetch request to the Flask API endpoint
        fetch('/api/keywords')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(keywords => {
            // Combine all keywords into a single array for easier iteration
            let combinedKeywords = [...keywords['FOOD'], ...keywords['GPE']];

            // Append combined keywords to the list for the user to choose
            combinedKeywords.forEach(function(keyword) {
                let listItem = document.createElement('li');
                listItem.textContent = keyword;
                listItem.addEventListener('click', function() {
                    let searchInput = document.getElementById('search-input');
                    searchInput.value = keyword; // On click, fill the search box with the keyword
                    // Optionally, you can trigger the search automatically
                    // searchInput.form.submit(); // Uncomment this line to submit the form automatically
                });
                keywordList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error fetching keywords:', error);
        });
    });
});



// // script.js
// document.getElementById('search-button').addEventListener('click', function(event) {
//     event.preventDefault();  // Prevent the default form submission
//     var searchValue = document.getElementById('search-input').value;

//     // Make an AJAX request to the Flask backend
//     fetch('/search', {
//         method: 'POST',
//         body: new URLSearchParams({'keywords': searchValue})
//     })
//     .then(response => {
//         if (response.ok) {
//             return response.text();  // Assuming the response is text/html
//         }
//         throw new Error('Network response was not ok.');
//     })
//     .then(html => {
//         // Update the page with the results
//         // You might update an element with ID 'results-section', for example
//         document.getElementById('results-section').innerHTML = html;
//     })
//     .catch(error => console.error('Error:', error));
// });

// JavaScript Code
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the plot with empty data and layout
    var graphPlaceholder = document.getElementById('graph-placeholder');
    Plotly.newPlot(graphPlaceholder, [], {});

    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission
        console.log("Form submitted");  // Log the submission for debugging
        var searchValue = document.getElementById('search-input').value;

        // Make an AJAX request to the Flask backend
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'keywords': searchValue})
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            console.log("Received graph data:", data);  // Log the received data for debugging
            if (!data || !data.graph_html) {
                console.error("Invalid data received", data);
                return;  // Handle the lack of data appropriately
            }

            // Use Plotly.react to update the plot with new data
            const graphData = JSON.parse(data.graph_html);
            Plotly.react(graphPlaceholder, graphData.data, graphData.layout);
        });
    });
});