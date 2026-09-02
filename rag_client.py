import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories matching pattern chroma*
    chroma_dirs = list(current_dir.glob("chroma*"))

    # Loop through each discovered directory
    for chroma_dir in chroma_dirs:
        try:
            # Wrap connection attempt in try-except block for error handling
            if not chroma_dir.is_dir():
                continue
            
            # Initialize database client with directory path and configuration settings
            client = chromadb.PersistentClient(path=str(chroma_dir))
            
            # Retrieve list of available collections from the database
            collections = client.list_collections()
            
            # Loop through each collection found
            for collection in collections:
                # Create unique identifier key combining directory and collection names
                key = f"{chroma_dir.name}_{collection.name}"
                
                # Build information dictionary containing all necessary information
                try:
                    doc_count = collection.count()
                except:
                    doc_count = "unknown"
                
                backends[key] = {
                    # Store directory path as string
                    "directory": str(chroma_dir),
                    # Store collection name
                    "collection_name": collection.name,
                    # Create user-friendly display name
                    "display_name": f"{chroma_dir.name} - {collection.name} ({doc_count} docs)",
                    # Get document count with fallback for unsupported operations
                    "doc_count": doc_count
                }
        
        except Exception as e:
            # Handle connection or access errors gracefully
            error_msg = str(e)[:50]  # Truncate error message
            backends[f"{chroma_dir.name}_error"] = {
                # Create fallback entry for inaccessible directories
                "directory": str(chroma_dir),
                "collection_name": "error",
                # Include error information in display name with truncation
                "display_name": f"{chroma_dir.name} (Error: {error_msg}...)",
                # Set appropriate fallback values for missing information
                "doc_count": 0
            }

    # Return complete backends dictionary with all discovered collections
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # Create a chromadb persistent client
    client = chromadb.PersistentClient(path=chroma_dir)
    
    # Return the collection with the collection_name
    return client.get_collection(name=collection_name)

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # Initialize filter variable to None (represents no filtering)
    where_filter = None

    # Check if filter parameter exists and is not set to "all" or equivalent
    if mission_filter and mission_filter.lower() != "all":
        # Create filter dictionary with appropriate field-value pairs
        where_filter = {"mission": mission_filter}

    # Execute database query with the following parameters
    results = collection.query(
        # Pass search query in the required format
        query_texts=[query],
        # Set maximum number of results to return
        n_results=n_results,
        # Apply conditional filter (None for no filtering, dictionary for specific filtering)
        where=where_filter
    )

    # Return query results to caller
    return results

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # Initialize list with header text for context section
    context_parts = ["=== Retrieved Context ==="]

    # Loop through paired documents and their metadata using enumeration
    for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
        # Extract mission information from metadata with fallback value
        mission = metadata.get('mission', 'Unknown Mission')
        # Clean up mission name formatting (replace underscores, capitalize)
        mission_display = mission.replace('_', ' ').title()
        
        # Extract source information from metadata with fallback value
        source = metadata.get('source', 'Unknown Source')
        # Extract category information from metadata with fallback value
        category = metadata.get('document_category', 'General')
        # Clean up category name formatting (replace underscores, capitalize)
        category_display = category.replace('_', ' ').title()
        
        # Create formatted source header with index number and extracted information
        source_header = f"\n[Source {i+1}] {mission_display} - {source} ({category_display})"
        # Add source header to context parts list
        context_parts.append(source_header)
        
        # Check document length and truncate if necessary
        max_doc_length = 500
        if len(doc) > max_doc_length:
            # Add truncated document content to context parts list
            context_parts.append(f"{doc[:max_doc_length]}...")
        else:
            # Add full document content to context parts list
            context_parts.append(doc)

    # Join all context parts with newlines and return formatted string
    return "\n".join(context_parts)