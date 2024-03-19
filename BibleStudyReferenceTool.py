import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io


def create_pdf(output_text, notes):
    """Generate a PDF file containing the given text and notes with text wrapping."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    # Add output text and notes as paragraphs to ensure proper text wrapping
    for text in output_text.strip().split('\n'):
        flowables.append(Paragraph(text, styles['Normal']))
        flowables.append(Spacer(1, 12))  # Add space between paragraphs

    # Add a heading for the notes
    flowables.append(Paragraph("Notes:", styles['Heading2']))

    # Split notes into lines to handle very long text properly
    note_lines = notes.strip().split('\n')
    for line in note_lines:
        flowables.append(Paragraph(line, styles['Normal']))
        flowables.append(Spacer(1, 12))

    doc.build(flowables)
    buffer.seek(0)
    return buffer


def main():
    st.title('Bible Study Reference Tool')

    # Create input fields for book, chapter, verse, first witness, second witness, and notes
    book = st.text_input("Book:")
    chapter = st.text_input("Chapter:")
    verse = st.text_input("Verse:")
    first_witness = st.text_input("First Witness:")
    second_witness = st.text_input("Second Witness:")
    notes = st.text_area("Notes:")

    # Display inputs or perform action based on the inputs
    if st.button("Submit"):
        if book and chapter and verse and first_witness and second_witness:
            # Format the output text
            output_text = f"Book: {book}\nChapter: {chapter}\nVerse: {verse}\nFirst Witness: {first_witness}\nSecond Witness: {second_witness}"
            st.markdown(output_text.replace('\n', '<br>'), unsafe_allow_html=True)

            # Generate PDF including notes
            pdf = create_pdf(output_text, notes)

            # Download button for the PDF
            st.download_button(
                label="Download as PDF",
                data=pdf,
                file_name="bible_references_notes.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please enter the book, chapter, verse, witnesses, and notes.")


if __name__ == "__main__":
    main()
