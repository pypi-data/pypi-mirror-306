from act_workflow.act.nodes.e2bsandbox_node import E2BSandboxNode
from page_node import PageNode
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the E2B Sandbox
e2b_sandbox = E2BSandboxNode()
e2b_sandbox_result = e2b_sandbox.execute({})

if e2b_sandbox_result['status'] == 'success':
    # List to keep track of all pages
    pages = []

    # Function to create a new page
    def create_page(name, title, page_content, api_content):
        test_data = {
            "e2b_sandbox_node": e2b_sandbox,
            "page_name": name,
            "operation": "create",
            "content": page_content,
            "variable_mappings": {"title": title}
        }

        page_node = PageNode()
        result = page_node.execute(test_data)
        
        if result['status'] == 'success':
            pages.append({"name": name, "title": title})
            print(f"Created page: {result['result']['page_url']}")
        else:
            print(f"Failed to create page {name}: {result['message']}")

    # Create home page with menu
    def create_home_page():
        menu_items = "".join([f'<li><a href="/{page["name"]}">{page["title"]}</a></li>' for page in pages])
        home_page_content = f"""
    import React from 'react';

    export default function HomePage() {{
        return (
            <div>
                <h1>Welcome to Our Next.js Site</h1>
                <nav>
                    <ul>
                        {menu_items}
                    </ul>
                </nav>
            </div>
        );
    }}
    """
        create_page("", "Home", home_page_content, "")

    # Create pages
    create_page("about", "About Us", 
    """
    import React from 'react';
    import Link from 'next/link';

    export default function AboutPage() {
        return (
            <div>
                <h1>About Us</h1>
                <p>This is the about page.</p>
                <Link href="/">Back to Home</Link>
            </div>
        );
    }
    """, "")

    create_page("contact", "Contact Us", 
    """
    import React from 'react';
    import Link from 'next/link';

    export default function ContactPage() {
        return (
            <div>
                <h1>Contact Us</h1>
                <p>Get in touch with us here.</p>
                <Link href="/">Back to Home</Link>
            </div>
        );
    }
    """, "")

    create_page("services", "Our Services", 
    """
    import React from 'react';
    import Link from 'next/link';

    export default function ServicesPage() {
        return (
            <div>
                <h1>Our Services</h1>
                <ul>
                    <li>Service 1</li>
                    <li>Service 2</li>
                </ul>
                <Link href="/">Back to Home</Link>
            </div>
        );
    }
    """, "")

    # Create home page with menu after other pages are created
    create_home_page()

    print(f"\nE2B Sandbox Node initialized. Public URL: {e2b_sandbox.public_url}")
    print("You can now access the following pages:")
    for page in pages:
        print(f"- {page['title']}: {e2b_sandbox.public_url}/{page['name']}")

    # Keep the server running for a while
    print("\nThe app will run for 10 minutes. You can open it in your browser.")
    time.sleep(600)

    e2b_sandbox.close()
else:
    print(f"Failed to initialize E2BSandboxNode: {e2b_sandbox_result['message']}")