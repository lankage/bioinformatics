package com.ocl.pivotmappingcounts;

import com.biomatters.geneious.publicapi.components.Dialogs;
import com.biomatters.geneious.publicapi.documents.AnnotatedPluginDocument;
import com.biomatters.geneious.publicapi.documents.DocumentUtilities;
import com.biomatters.geneious.publicapi.documents.PluginDocument;
import com.biomatters.geneious.publicapi.documents.SummaryDocument;
import com.biomatters.geneious.publicapi.documents.sequence.AminoAcidSequenceDocument;
import com.biomatters.geneious.publicapi.documents.sequence.NucleotideSequenceDocument;
import com.biomatters.geneious.publicapi.documents.sequence.SequenceAlignmentDocument;
import com.biomatters.geneious.publicapi.documents.sequence.SequenceDocument;
import com.biomatters.geneious.publicapi.implementations.DefaultAlignmentDocument;
import com.biomatters.geneious.publicapi.implementations.sequence.DefaultAminoAcidSequence;
import com.biomatters.geneious.publicapi.implementations.sequence.DefaultNucleotideGraphSequence;
import com.biomatters.geneious.publicapi.implementations.sequence.DefaultNucleotideSequence;
import com.biomatters.geneious.publicapi.plugin.*;
import com.biomatters.geneious.publicapi.utilities.IconUtilities;

import jebl.util.ProgressListener;

import java.awt.Toolkit;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.ImageIcon;

/**
 * @author Michael Graham
 * @version $Id: PivotMappingCountsPlugin.java
 */
public class PivotMappingCountsPlugin extends GeneiousPlugin {

	private StringBuilder outputText; // text contents

	public String getName() {
		return "Pivot Mapping Counts";
	}

	public String getDescription() {
		return "Generate text file with mapped read counts for each barcode / refseq combination";
	}

	public String getHelp() {
		return null;
	}

	public String getAuthors() {
		return "Michael Graham";
	}

	public String getVersion() {
		return "1.0";
	}

	public DocumentOperation[] getDocumentOperations() {
		return new DocumentOperation[]{pivotCounts};
	}

	private DocumentOperation pivotCounts = new DocumentOperation() {
		@Override
		public List<AnnotatedPluginDocument> performOperation(AnnotatedPluginDocument[] documents, ProgressListener progressListener, Options options) throws DocumentOperationException {
			Map<String, Map<String, Integer>> countsDictionary = new HashMap<String, Map<String, Integer>>();
			Collection<String> allAllelesDict = new TreeSet<String>(Collator.getInstance());
			outputText = new StringBuilder();

			for (AnnotatedPluginDocument doc : documents) {

				//final AnnotatedPluginDocument doc = documents[0];
				final DefaultAlignmentDocument alnDoc = (DefaultAlignmentDocument) doc.getDocument();

				//contig name of assembled alignment file
				final String contigName = alnDoc.getName();
				// System.out.println(contigName);

				List<String> barcodesLocal = new ArrayList<String>();

				List<SequenceDocument> contigSequences = alnDoc.getSequences();
				for (int i = 1; i < contigSequences.size(); i++) {
					String currentSeqName = contigSequences.get(i).getName();
					//System.out.println(currentSeqName);
					String[] whiteStrip = currentSeqName.split(" ");
					String[] nameParts = whiteStrip[0].split("/");
					String lastpart = nameParts[nameParts.length - 1];
					//System.out.println(lastpart);
					String[] extensionParts = lastpart.split("\\.");
					String barcodeName = "";
					if (extensionParts.length > 0) {
						barcodeName = extensionParts[0];
					}
					else {
						barcodeName = lastpart;
					}

					//System.out.println(barcodeName);
					barcodesLocal.add(barcodeName);

				}
				String barcodeTester = barcodesLocal.get(0);

				if( barcodeTester.length() > 1) {
					for (int i = 0; i < barcodesLocal.size(); i++) {
						//System.out.println(barcodes.get(i));
						String bc = barcodesLocal.get(i);

						if (countsDictionary.get(bc) == null) {
							Map<String, Integer> alleleCountsDict = new HashMap<String, Integer>();
							alleleCountsDict.put(contigName, 1);
							countsDictionary.put(bc, alleleCountsDict);
						} else if (countsDictionary.get(bc).get(contigName) == null ) {

							countsDictionary.get(bc).put(contigName, 1);

						}
						else {
							Integer currentCount = countsDictionary.get(bc).get(contigName);
							Integer newCount = currentCount + 1;
							countsDictionary.get(bc).put(contigName, newCount);
						}

					}

				}


			}
			// unroll it for pivoting

			//Make alleles dictionary for first column
			for (String barcode : countsDictionary.keySet()) {
				for (String allele : countsDictionary.get(barcode).keySet()) {
					if (!allAllelesDict.contains(allele)) {
						allAllelesDict.add(allele);
					}

				}	


			}
			// Print out column headers (barcode names)
			String pattern = ":|Contig";
			Pattern r = Pattern.compile(pattern);


			System.out.print("Allele_Name\t");
			outputText.append("Allele_Name\t");
			Collection<String> barcodesSorted = new TreeSet<String>(Collator.getInstance());
			for (String barcode : countsDictionary.keySet()) {

				//
				Matcher m = r.matcher(barcode);
				if (m.find()) {
					//System.out.println(barcode);
					Integer i = 0;
				}
				else {
					barcodesSorted.add(barcode);
				}

			}
			for (String barcode : barcodesSorted) {
				System.out.print(barcode + "\t");
				outputText.append(barcode + "\t");
			}
			System.out.println("");
			outputText.append("\n");
			for (String aName : allAllelesDict) {
				System.out.print(aName + "\t");
				outputText.append(aName + "\t");
				for (String barcode : barcodesSorted) {
					if (countsDictionary.get(barcode).containsKey(aName) && barcodesSorted.contains(barcode)) {
						outputText.append(countsDictionary.get(barcode).get(aName) + "\t");
						System.out.print(countsDictionary.get(barcode).get(aName) + "\t");


					}
					else {
						outputText.append("\t");
						System.out.print("\t");
					}


				}
				outputText.append("\n");
				System.out.println("");
			}


			final Date date = new Date();

			String finalString = outputText.toString();
			TextDocument tableOutput = new TextDocument("PivotTable.txt",date,finalString);

			List<PluginDocument> results = new ArrayList<PluginDocument>();
			//results.add(countsDoc);
			results.add(tableOutput);
			return DocumentUtilities.createAnnotatedPluginDocuments(results);


		}

		public GeneiousActionOptions getActionOptions() {
			//String imageFile = "/PivotMappingCounts/images/robot_small.jpg";
			//java.net.URL imgUrl = PivotMappingCountsPlugin.class.getResource("robot_small.jpg");
			//ImageIcon icon = new ImageIcon(Toolkit.getDefaultToolkit().createImage(imgUrl));
			//Icons robotIcon = IconUtilities.getIconsFromJar(PivotMappingCountsPlugin.class, "/robot_icon_small.png");
			Icons robotIcon = IconUtilities.getIconsFromJar(PivotMappingCountsPlugin.class, "/robot_icon_small.png");
			//Icons icons = new Icons(icon);
			return new GeneiousActionOptions("Activate Pivotron", "Generate table of mapping counts",
					robotIcon, GeneiousActionOptions.Category.None).setInMainToolbar(true);
		}

		public String getHelp() {
			return "Pivotron expects a contig alignment file. (The one with the three red lines)";
		}

		public DocumentSelectionSignature[] getSelectionSignatures() {
			DocumentSelectionSignature sequenceAlignmentSignature = new DocumentSelectionSignature(SequenceAlignmentDocument.class, 1, 1000);

			return new DocumentSelectionSignature[]{sequenceAlignmentSignature};
		}

		@Override
		public Options getOptions(final AnnotatedPluginDocument... documents) {
			return null;
		}
	};

	public String getMinimumApiVersion() {
		return "4.0";
	}

	public int getMaximumApiVersion() {
		return 4;
	}
}
