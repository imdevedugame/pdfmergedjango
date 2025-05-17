# Pseudofile - PDF Processing Cloud Service

Pseudofile is a cloud-based PDF processing service that allows users to convert, compress, merge, and store PDF files. The application is built with Streamlit for the frontend and uses Supabase for authentication, database, and storage.

## Features

- **PDF Convert**: Convert various document formats (Word, images, text) to PDF
- **PDF Compress**: Reduce PDF file size without significant quality loss
- **PDF Merge**: Combine multiple PDF files into a single document
- **PDF Pocket**: Store and manage processed PDF files in the cloud
- **User Authentication**: Secure login and registration
- **Usage Tracking**: Monitor and limit daily usage
- **Billing Simulation**: Calculate costs based on usage

## Project Structure

\`\`\`
pseudofile/
├── frontend/             # Streamlit UI components
│   ├── app.py            # Main Streamlit application
│   ├── pages/            # UI for different pages
│   ├── components/       # Reusable UI components
│   └── styles/           # CSS styles
├── backend/              # Backend logic
│   ├── auth.py           # Authentication functions
│   ├── database.py       # Database interactions
│   ├── storage.py        # File storage operations
│   └── pdf/              # PDF processing functions
├── database/             # Database schema and initialization
├── .env                  # Environment variables (not in repo)
├── .env.example          # Example environment variables
├── requirements.txt      # Project dependencies
└── main.py               # Application entry point
\`\`\`

## Setup Instructions

1. **Clone the repository**

\`\`\`bash
git clone https://github.com/yourusername/pseudofile.git
cd pseudofile
\`\`\`

2. **Set up environment variables**

Copy the example environment file and update with your Supabase credentials:

\`\`\`bash
cp .env.example .env
# Edit .env with your credentials
\`\`\`

3. **Install dependencies**

\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Initialize the database**

Run the database initialization script to set up the schema:

\`\`\`bash
python database/init_db.py
\`\`\`

5. **Run the application**

\`\`\`bash
streamlit run main.py
\`\`\`

## Supabase Setup

1. Create a new Supabase project
2. Set up authentication with email/password
3. Create the database tables using the SQL in `database/schema.sql`
4. Create a storage bucket named "files" with public access
5. Copy your Supabase URL and API key to the `.env` file

## Usage Limits

- PDF Convert: 3 conversions per day
- PDF Compress: 3 compressions per day
- PDF Merge: 3 merges per day

## Billing

- Conversions: Rp100 per operation
- Compressions: Rp100 per operation
- Merges: Rp200 per operation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
