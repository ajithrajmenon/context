# -*- coding: utf-8 -*-
"""The long layer.

Every story links to one of these. The story is the public face; the paper is
what earns it the right to be believed. See STYLE.md section 6 — nobody has to
read the paper, everybody has to be able to.

Each paper carries:
    abstract     what we set out to establish and what we found
    sections     the body, by heading
    findings     numbered, each with a confidence level we are willing to defend
    contested    the live disagreements, stated as disagreements
    unknowns     what we could not establish
    method       how the work was done and what it did not include
    reading      real sources, each described so a reader knows what it is for

Confidence levels are deliberately only three: 'established', 'best current
explanation', 'contested'. More gradations would be false precision.
"""

PAPERS = [

# ------------------------------------------------------------------ sleep
{
 'slug': 'why-do-we-sleep',
 'title': 'Sleep: what it costs to lose it, and why you cannot tell',
 'subtitle': 'A review of what is well established about sleep function and sleep '
             'restriction, and where the popular account runs ahead of the evidence.',
 'date': 'August 2026',
 'minutes': 12,

 'abstract':
   'We set out to answer a narrow question: is the widely repeated claim that people '
   '“adapt” to short sleep true in any sense? It is true in one sense and false in the '
   'sense that matters. Subjective sleepiness plateaus within a few days of restriction '
   'while objective performance continues to decline — the two measures come apart, and '
   'people are left confidently unaware of an ongoing deficit. We also found that the '
   'most-repeated mechanistic claim in popular sleep writing (that sleep exists to clear '
   'brain waste) is on considerably softer ground than its retelling suggests.',

 'sections': [
   {'h': 'Why the question is hard',
    'p': ['Sleep research has an unusual problem: the outcome most people care about — '
          'how they feel — is measured by asking the person, and the person is the thing '
          'under test. A sleep-deprived participant is being asked to assess their own '
          'judgement using the faculty being degraded.',
          'This is why the field leans on objective tasks. The psychomotor vigilance '
          'task, essentially a reaction-time test with no learning curve, has become the '
          'standard instrument precisely because it is boring, unlearnable and sensitive.']},

   {'h': 'The dissociation',
    'p': ['The finding that reorganised how the field talks about sleep debt came from '
          'chronic restriction studies in the early 2000s, most influentially the '
          'protocol run by Van Dongen and colleagues (2003), in which adults were held '
          'at four, six or eight hours in bed for two weeks.',
          'The six-hour group is the interesting one. After two weeks their objective '
          'performance had degraded to roughly what a night of total sleep deprivation '
          'produces. Their self-rated sleepiness had risen for a few days and then '
          'largely levelled off.',
          'That is the whole result, and it is unusually clean: the subjective signal '
          'saturates while the objective decline continues. It is not that people lie '
          'about being tired. It is that the internal gauge stops tracking the thing it '
          'is meant to measure.']},

   {'h': 'What sleep is for',
    'p': ['There is no single accepted answer, and anyone presenting one is compressing. '
          'The serious candidates are not mutually exclusive and probably all contribute: '
          'energy conservation, immune function, synaptic downscaling, and memory '
          'consolidation.',
          'Memory consolidation has the strongest experimental support of the four. The '
          'observation that sleep after learning improves later recall replicates widely '
          'across task types and species.',
          'Waste clearance — the claim that fluid flow through the brain increases during '
          'sleep and removes metabolic by-products — entered public writing extremely '
          'fast after Xie and colleagues published in 2013. It is a real and interesting '
          'result. It is also a mouse result, with methodological disputes about whether '
          'anaesthesia rather than sleep drove the effect, and the human evidence remains '
          'thinner than the confidence of its retelling.']},

   {'h': 'Architecture',
    'p': ['A night proceeds in cycles of roughly ninety minutes, though the figure varies '
          'considerably between people and across the night. Slow-wave sleep dominates '
          'early cycles; REM periods lengthen toward morning.',
          'The practical consequence of that asymmetry is asymmetric loss. Cutting a night '
          'short at the end removes disproportionately more REM; going to bed late removes '
          'disproportionately more slow-wave sleep. "Six hours" is therefore not one '
          'condition but two, depending on which end you take it from — a distinction most '
          'popular writing skips.']},
 ],

 'findings': [
   ('Subjective sleepiness stops tracking objective impairment under chronic restriction.',
    'established',
    'Replicated across several restriction protocols. This is the single most decision-relevant finding in the literature.'),
   ('Around seven to nine hours suits most adults, with real individual variation.',
    'established',
    'Consensus position of the major sleep societies. The variation is genuine, but far smaller than people claim for themselves.'),
   ('Sleep after learning improves subsequent recall.',
    'established',
    'Robust across task types, ages and species.'),
   ('One long lie-in does not clear an accumulated week of restriction.',
    'best current explanation',
    'Recovery of some measures is fast; others lag for days. Full-recovery timelines are not well characterised.'),
   ('Fluid clearance of brain waste increases during sleep.',
    'contested',
    'Striking initial rodent result; methodological disputes unresolved and human evidence limited.'),
   ('Genuine short sleepers exist, carrying rare variants.',
    'established',
    'Real but very rare. Almost everyone who believes they are one is not.'),
 ],

 'contested': [
   ('Does sleep exist primarily to clear metabolic waste?',
    'The 2013 glymphatic work made this the popular answer within about two years. '
    'Subsequent work has questioned whether the effect is driven by sleep or by the '
    'anaesthetic used, and at least one later study reported reduced rather than '
    'increased clearance during sleep. The honest position is that this is an active '
    'and unsettled area being reported as though it were closed.'),
   ('How much of the harm attributed to short sleep is causal?',
    'Long-run associations between short sleep and cardiovascular and metabolic disease '
    'are consistent, but much of the evidence is observational and reverse causation is '
    'plausible — early illness disrupts sleep. Effect sizes from experiments are smaller '
    'than the associations imply.'),
 ],

 'unknowns': [
   'Why sleep is universal among animals with brains, in mechanistic rather than functional terms.',
   'The true recovery curve after chronic restriction, measure by measure.',
   'Whether the subjective/objective dissociation can be trained away or compensated for. Current evidence suggests not.',
 ],

 'method':
   'This is a synthesis of published work, not new research. We prioritised experimental '
   'restriction protocols over observational cohorts wherever both addressed the same '
   'question, and we treated any mechanistic claim resting on a single striking result as '
   'provisional regardless of how widely it has been repeated. We did not conduct a '
   'systematic review, and we did not attempt to weight studies by sample size. Where the '
   'story states a number, it is the central figure from the sources below, rounded.',

 'reading': [
   ('Van Dongen, Maislin, Mullington & Dinges (2003), “The cumulative cost of additional wakefulness”, Sleep',
    'The chronic restriction protocol behind the central finding. Read the figures if nothing else — the divergence between the subjective and objective lines is the entire story.'),
   ('Xie et al. (2013), “Sleep drives metabolite clearance from the adult brain”, Science',
    'The origin of the waste-clearance account. Worth reading alongside its critics rather than alone.'),
   ('Walker, Why We Sleep (2017)',
    'The book that put sleep on the public agenda. Compelling and useful, but several claims are stated far more firmly than the underlying evidence supports; read it with that in mind.'),
   ('Consensus statements of the American Academy of Sleep Medicine and Sleep Research Society',
    'The dull, careful, institutional position on duration recommendations. A good corrective to any single dramatic study.'),
 ],
},

# ------------------------------------------------------------------ death
{
 'slug': 'what-happens-when-you-die',
 'title': 'Death as a process: why the moment had to be redefined',
 'subtitle': 'How a definition that held for millennia broke within a decade, and what '
             'replaced it.',
 'date': 'August 2026',
 'minutes': 11,

 'abstract':
   'We set out to establish how much of the popular picture of death as an instant '
   'survives contact with clinical practice. Very little of it does. Death is a sequence '
   'with a reliable order and a duration measured in hours; the legal and clinical '
   'definition moved to the brain in the mid-twentieth century specifically because '
   'resuscitation made the older cardiac definition unworkable. The organ-viability '
   'windows that make transplantation possible are a direct consequence.',

 'sections': [
   {'h': 'A definition that stopped working',
    'p': ['For almost all of recorded history, death meant the heart had stopped. This '
          'was not a philosophical position so much as a practical one: it was observable, '
          'and it was irreversible.',
          'Two developments in the mid-twentieth century removed the second property. '
          'Closed-chest cardiac massage and external defibrillation made cardiac arrest '
          'frequently reversible. Mechanical ventilation made it possible to maintain '
          'circulation and oxygenation in a body whose brain had ceased functioning '
          'entirely.',
          'The result was a category the old definition could not name: bodies that were '
          'warm, perfused and metabolically active, in which nothing that could be called '
          'a person remained.']},

   {'h': 'The move to the brain',
    'p': ['The 1968 report of the Harvard Ad Hoc Committee proposed criteria for '
          'irreversible coma as a definition of death. In the United States this was '
          'eventually formalised in the Uniform Determination of Death Act (1981), which '
          'admits two routes: irreversible cessation of circulatory and respiratory '
          'function, or irreversible cessation of all functions of the entire brain.',
          'The logic behind the choice is worth stating plainly, because it is often '
          'presented as arbitrary. The brain was selected not because consciousness is '
          'metaphysically privileged but because it is the only organ for which there is '
          'no replacement, no restart and no bridge. Everything else can be substituted, '
          'transplanted or mechanically supported.']},

   {'h': 'The sequence',
    'p': ['Once circulation stops, tissues fail in an order set by their oxygen demand '
          'and their tolerance of ischaemia. Neurons are the most demanding tissue in the '
          'body by a wide margin; consciousness is lost within seconds and irreversible '
          'injury begins within minutes.',
          'Most other tissue is far more tolerant. This is not a curiosity — it is the '
          'entire operating basis of transplantation, and the reason a single donor can '
          'result in several recipients. The viability windows are approximate, depend '
          'heavily on preservation technique, and have been extended significantly by '
          'machine perfusion.']},

   {'h': 'Where the popular account goes wrong',
    'p': ['Two errors recur. The first is treating death as instantaneous, which makes '
          'organ donation look ghoulish rather than logistically obvious.',
          'The second is the widely repeated claim that hair and nails continue to grow '
          'after death. They do not. The skin retracts as it dehydrates, exposing more of '
          'the shaft. The observation is real; the explanation is wrong.']},
 ],

 'findings': [
   ('Death is a sequence with a reliable order, not a single event.',
    'established',
    'Uncontroversial in clinical medicine; almost absent from the popular picture.'),
   ('Consciousness is lost within roughly ten seconds of circulatory arrest.',
    'established',
    'Consistent with cerebral oxygen reserves and observed directly in cardiac arrest and in centrifuge studies.'),
   ('Organ viability windows range from minutes for brain tissue to days for cornea.',
    'established',
    'Figures are approximate, vary with preservation method, and have lengthened with machine perfusion.'),
   ('The definition of death moved to the brain because resuscitation broke the cardiac criterion.',
    'established',
    'Documented directly in the Harvard committee report and the legislative record.'),
   ('Hair and nails do not continue growing after death.',
    'established',
    'The appearance is caused by retraction of dehydrating skin.'),
   ('Brain activity in the minutes around death follows a characteristic pattern.',
    'contested',
    'Reported in small numbers of incidental human recordings and in animal models. Interesting, widely over-interpreted, and nowhere near sufficient to support claims about experience.'),
 ],

 'contested': [
   ('Is whole-brain death the right criterion, or is higher-brain function the relevant one?',
    'A genuine and unresolved dispute in bioethics. Whole-brain criteria are the legal '
    'standard in most jurisdictions, but critics argue they are neither biologically '
    'coherent nor consistently applied, since some hypothalamic function can persist.'),
   ('What, if anything, do surges of brain activity around death correspond to?',
    'A small number of recordings have shown organised activity in the period around '
    'cardiac arrest. These are incidental, uncontrolled, and involve injured brains. '
    'They have been used to support strong claims about near-death experience that they '
    'cannot carry.'),
 ],

 'unknowns': [
   'The upper bound on viability for most organs under optimal preservation — it keeps moving.',
   'Whether any subjective experience accompanies the terminal period, and whether that is answerable even in principle.',
   'How consistently brain-death criteria are applied across jurisdictions in practice.',
 ],

 'method':
   'Synthesis of clinical and legal literature. We treated transplantation practice as the '
   'strongest available evidence about viability windows, on the grounds that it is '
   'operational rather than theoretical — those numbers are used to make decisions under '
   'time pressure. We deliberately excluded near-death-experience literature from the '
   'findings, as the reporting is retrospective and unblinded. We did not consult '
   'jurisdiction-by-jurisdiction legal definitions beyond the United States and United '
   'Kingdom.',

 'reading': [
   ('Report of the Ad Hoc Committee of the Harvard Medical School (1968), JAMA',
    'The document that started the redefinition. Short, readable, and startlingly candid about its own motivations.'),
   ('Uniform Determination of Death Act (1981)',
    'The legal text. Worth reading for how carefully it avoids saying what death *is*.'),
   ('Truog & Miller, “The dead donor rule and organ transplantation”, NEJM (2008)',
    'The most-cited challenge to the coherence of current brain-death criteria. Uncomfortable and well argued.'),
   ('Guidance from national transplant services on organ retrieval timings',
    'Operational documents rather than papers, and the best source for viability figures because the numbers carry consequences.'),
 ],
},

# ------------------------------------------------------------------ immune
{
 'slug': 'the-war-inside-you',
 'title': 'Why illness feels the way it does',
 'subtitle': 'The symptoms of infection are largely the response, not the pathogen — '
             'and what follows from taking that seriously.',
 'date': 'August 2026',
 'minutes': 13,

 'abstract':
   'We set out to establish how much of what a person experiences during a common '
   'infection is caused by the pathogen and how much by their own immune response. For '
   'most common infections the answer is that the response dominates. This reframes '
   'fever, swelling and malaise as functional rather than incidental, and it has direct '
   'consequences for how we think about symptom suppression and about vaccine side '
   'effects.',

 'sections': [
   {'h': 'Three layers, not one system',
    'p': ['It is more useful to think of immunity as three systems with different '
          'timescales than as a single thing. Physical and chemical barriers operate '
          'continuously. Innate responses act within minutes to hours and are not '
          'specific. Adaptive responses take days to develop, are exquisitely specific, '
          'and persist.',
          'Almost everything is stopped by the first layer, which is why the reader has '
          'no experience of it. You only ever become aware of the failures.']},

   {'h': 'The symptoms are the response',
    'p': ['The classical signs of inflammation — heat, redness, swelling, pain — are all '
          'produced by the host. Vasodilation increases blood flow to the affected tissue; '
          'increased vascular permeability lets cells and fluid into it; inflammatory '
          'mediators sensitise nociceptors.',
          'Fever is host-generated, metabolically expensive, and conserved across an '
          'enormous evolutionary range, which is a strong argument that it does something '
          'useful. There is reasonable evidence that moderate fever impairs replication of '
          'some pathogens and enhances several immune functions.',
          'This does not license refusing antipyretics. The honest position is that '
          'suppressing moderate fever for comfort is unlikely to be very harmful and is '
          'unlikely to be very helpful, and that the evidence on whether it prolongs '
          'illness is genuinely mixed.']},

   {'h': 'Memory, and what a vaccine borrows',
    'p': ['The adaptive response leaves behind long-lived memory cells. A second encounter '
          'with the same pathogen is met faster and harder, often before symptoms develop.',
          'A vaccine induces that memory without the danger, by presenting the immune '
          'system with a component of the pathogen, or instructions for making one, rather '
          'than the replicating organism.',
          'The soreness and fatigue that follow are therefore not side effects in the '
          'usual sense. They are the innate response doing exactly what it does after any '
          'immunological challenge — the same machinery, running without the disease. '
          'Their absence does not indicate failure, and their presence does not indicate '
          'a stronger result.']},

   {'h': 'Why a well-trained system matters',
    'p': ['Early-life exposure appears to be important for calibrating what the immune '
          'system treats as a threat. The observation that allergic and autoimmune '
          'conditions have risen alongside improvements in sanitation motivated the '
          '“hygiene hypothesis”.',
          'The name has aged badly. The current formulations emphasise diversity of '
          'microbial exposure — particularly in the gut, and particularly early — rather '
          'than cleanliness as such. Nothing in this literature is an argument against '
          'handwashing.']},
 ],

 'findings': [
   ('The bulk of common-infection symptoms are host-generated.',
    'established',
    'Uncontroversial mechanistically. The inflammatory signs are produced by host responses.'),
   ('Fever is an active, expensive, evolutionarily conserved response.',
    'established',
    'Conservation across a very wide range of taxa is strong evidence of function.'),
   ('Immunological memory underlies both natural immunity and vaccination.',
    'established',
    'The central result of twentieth-century immunology.'),
   ('Post-vaccination soreness is the innate response, not a marker of efficacy.',
    'established',
    'Reaction intensity correlates poorly with protection at the individual level.'),
   ('Suppressing moderate fever meaningfully prolongs common illness.',
    'contested',
    'Plausible mechanistically; trials are mixed, mostly small, and effect sizes where found are modest.'),
   ('Microbial exposure in early life shapes later allergic risk.',
    'best current explanation',
    'Consistent epidemiology and a plausible mechanism; specific causal pathways remain unclear.'),
 ],

 'contested': [
   ('Should moderate fever be treated?',
    'Mechanistic reasoning favours leaving it alone; clinical trial evidence is mixed and '
    'mostly underpowered. Clinical guidance generally prioritises comfort, which is a '
    'defensible reading of weak evidence rather than a strong finding.'),
   ('What exactly the hygiene hypothesis has become.',
    'The original framing is largely abandoned. Successors emphasise microbial diversity, '
    'the gut microbiome and specific early exposures, but they disagree with each other '
    'and the epidemiology admits several readings.'),
 ],

 'unknowns': [
   'Why immunological memory persists for decades against some pathogens and months against others.',
   'What determines whether an individual response is proportionate or damaging, which is the central question in severe infection.',
   'How much of adult immune variation is set in early life versus continuously remodelled.',
 ],

 'method':
   'Synthesis of standard immunology reference texts and review literature, with primary '
   'sources consulted for the two contested questions. We deliberately avoided drawing on '
   'single-trial results for anything stated as established. We did not review the clinical '
   'literature on antipyretic use systematically, and readers should treat our summary of '
   'that question as a characterisation of the disagreement rather than a verdict on it.',

 'reading': [
   ('Janeway’s Immunobiology (current edition)',
    'The standard text. The early chapters cover the three-layer structure better than any summary, including this one.'),
   ('Evans, Repasky & Fisher, “Fever and the thermal regulation of immunity”, Nature Reviews Immunology (2015)',
    'The best single review of what fever actually does. Careful about what is not known.'),
   ('Bloomfield et al., on the hygiene hypothesis and its successors',
    'Useful specifically because it addresses how badly the original name has served public understanding.'),
   ('Plotkin, “Correlates of protection induced by vaccination”, CVI (2010)',
    'Why reaction intensity is a poor proxy for protection. Directly relevant to the sore-arm question.'),
 ],
},

# ------------------------------------------------------------------ ageing
{
 'slug': 'why-do-we-age',
 'title': 'Ageing is not wear and tear',
 'subtitle': 'What the evidence supports about why bodies deteriorate, and which '
             'interventions survive scrutiny.',
 'date': 'August 2026',
 'minutes': 14,

 'abstract':
   'We set out to establish whether ageing is best understood as accumulated damage or as '
   'a programmed process, and to separate interventions with strong evidence from those '
   'with strong marketing. Neither framing is quite right: ageing is better described as '
   'the accumulation of specific, enumerable failures against a repair capacity that '
   'evolution has no reason to maintain past reproduction. Of the interventions we '
   'examined, the ones with the strongest evidence are also the least commercially '
   'interesting.',

 'sections': [
   {'h': 'Why "wearing out" cannot be the whole answer',
    'p': ['The intuition that bodies wear out like machines fails on a simple observation: '
          'machines are not continuously rebuilt and bodies are. Most tissue is replaced '
          'on timescales from days to a decade.',
          'It also fails comparatively. Lifespan varies enormously between species of '
          'similar size and metabolic rate, and some species show negligible increase in '
          'mortality rate with age. If ageing were straightforward physics, that variation '
          'would be difficult to explain.']},

   {'h': 'The evolutionary account',
    'p': ['The framework that makes sense of the variation is evolutionary. Selection '
          'pressure declines with age, because organisms are increasingly likely to have '
          'died of something else. Alleles with late-acting harmful effects are therefore '
          'weakly selected against.',
          'Antagonistic pleiotropy extends this: a variant that helps early and harms late '
          'can be positively selected. Ageing on this account is not a program but the '
          'predictable consequence of a maintenance budget that stops being worth paying.',
          'This explains the comparative data well. Species with low extrinsic mortality — '
          'those that fly, or live underground, or are very large — tend to live longer, '
          'because selection continues to act at later ages.']},

   {'h': 'The specific failures',
    'p': ['The influential synthesis here is the “hallmarks of ageing” framework proposed '
          'by López-Otín and colleagues in 2013 and revised since. It enumerates a set of '
          'processes including genomic instability, telomere attrition, epigenetic '
          'alteration, loss of proteostasis, mitochondrial dysfunction and cellular '
          'senescence.',
          'The framework is a useful organising device rather than a settled causal model. '
          'Its authors are explicit that the hallmarks interact and that their relative '
          'contributions are not established.',
          'Cellular senescence is the one that has moved fastest toward intervention. '
          'Senescent cells stop dividing but do not die, and secrete inflammatory factors. '
          'Clearing them extends healthy lifespan in mice. Whether this transfers to humans '
          'is being tested and is not yet known.']},

   {'h': 'What actually works',
    'p': ['The honest ranking is uncomfortable for the longevity industry. Not smoking, '
          'physical activity, adequate sleep, diet quality and social connection have '
          'evidence bases ranging from overwhelming to good.',
          'Almost nothing sold as an anti-ageing supplement survives a well-conducted '
          'trial. Caloric restriction extends lifespan reliably in several model organisms; '
          'the primate evidence is weaker and mixed, and the human evidence concerns '
          'biomarkers rather than lifespan.',
          'The gap between the strength of evidence and the volume of attention is, in this '
          'field, close to inverted.']},
 ],

 'findings': [
   ('Ageing is not primarily explained by passive wear.',
    'established',
    'Continuous tissue replacement and the comparative lifespan data both rule it out as a complete account.'),
   ('Declining selection pressure with age explains the comparative pattern.',
    'established',
    'The evolutionary framework has held up well and predicts the species data.'),
   ('Ageing involves multiple distinct, enumerable processes.',
    'best current explanation',
    'The hallmarks framework is widely adopted; relative causal weights are not settled.'),
   ('Senescent cells accumulate and contribute to tissue dysfunction.',
    'best current explanation',
    'Strong in mice, including clearance experiments. Human translation unproven.'),
   ('Not smoking, activity, sleep and diet quality meaningfully affect healthy lifespan.',
    'established',
    'Large, consistent effects across many cohorts.'),
   ('Any currently marketed supplement meaningfully extends human lifespan.',
    'contested',
    'We found no supplement with convincing human lifespan evidence. Several have suggestive biomarker data.'),
 ],

 'contested': [
   ('Do the hallmarks describe causes or symptoms?',
    'The framework enumerates processes that change with age. Which of them drive ageing '
    'and which are downstream is substantially unresolved, and different laboratories '
    'weight them very differently.'),
   ('Does caloric restriction extend human lifespan?',
    'Reliable in worms, flies and rodents. The two long-running primate studies reached '
    'different conclusions, which was eventually attributed largely to differences in the '
    'control diets. Human data concern biomarkers over short periods.'),
   ('Are biological-age clocks measuring ageing or correlating with it?',
    'Epigenetic clocks predict mortality better than chronological age. Whether they '
    'measure a causal process or track its consequences is unresolved, which matters '
    'enormously for their use as trial endpoints.'),
 ],

 'unknowns': [
   'Whether clearing senescent cells produces benefit in humans.',
   'Why some species show negligible senescence, in mechanistic terms.',
   'Whether the maximum human lifespan has a hard ceiling, and where it is.',
 ],

 'method':
   'Synthesis of review literature and comparative biology, with primary sources consulted '
   'for senescence clearance and caloric restriction. For the intervention ranking we '
   'weighted human evidence above model-organism evidence, and randomised evidence above '
   'observational, which systematically disadvantages newer interventions — that is a '
   'deliberate bias and readers should know about it. We did not conduct a meta-analysis, '
   'and the ranking reflects our reading of evidence strength rather than a computed effect size.',

 'reading': [
   ('López-Otín, Blasco, Partridge, Serrano & Kroemer, “The Hallmarks of Aging”, Cell (2013), and the 2023 revision',
    'The organising framework for the whole field. The revision is candid about what the original got wrong.'),
   ('Kirkwood, “Understanding the odd science of aging”, Cell (2005)',
    'The clearest short statement of the evolutionary account, by the person who developed much of it.'),
   ('Baker et al., on clearance of senescent cells in mice, Nature (2011, 2016)',
    'The experiments that made senescence a target rather than an observation.'),
   ('Mattison et al. (2017), Nature Communications, on the two primate caloric restriction studies',
    'The reconciliation of two studies that appeared to contradict each other. A good lesson in how much control conditions matter.'),
 ],
},

]

from stories_data import LIBRARY_PAPERS as _LP

PAPERS = PAPERS + _LP

BY_SLUG = {p['slug']: p for p in PAPERS}
