# Reporting a bug

P-KISS-SBC from PyFreeBilling project is an actively maintained project that we constantly strive
to improve. If you
think you have discovered a bug, you can help us by submitting an issue in our
public [issue tracker] by following this guide.

  [issue tracker]: https://github.com/mwolff44/pyfreebilling/issues

## Before creating an issue

The maintainers of this project are trying very hard to keep the number of open issues down by
fixing bugs as fast as possible. By following this guide, you will know exactly
what information we need to help you quickly.

__But first, please try the following things before creating an issue.__

### Upgrade to latest version

Chances are that the bug you discovered was already fixed in a subsequent
version. Thus, before reporting an issue, ensure that you're running the
[latest version] of P-KISS-SBC. Please consult our [upgrade guide] to
learn how to upgrade to the latest version.

!!! warning "Bug fixes are not backported"

    Please understand that only bugs that occur in the latest version of
    P-KISS-SBC will be addressed. Also, to reduce duplicate efforts,
    fixes cannot be backported to earlier versions.

### Remove customizations

If you're using customizations like Kamailio Modules, container modifications, or
specific diaplan, please remove them before reporting a bug.
We can't offer official support for bugs that might hide in your overrides.

If, after removing those settings, the bug is gone, the bug is likely caused by
your customizations. A good idea is to add them back gradually to narrow down
the root cause of the problem. If you did a major version upgrade, make sure you
adjusted all partials you have overridden.

__Don't be shy to ask on our [discussion board] for help if you run into
problems.__

  [latest version]: ../changelog/index.md
  [upgrade guide]: ../how-to/upgrade.md
  [discussion board]: https://github.com/mwolff44/pyfreebilling/discussions


### Search for solutions

At this stage, we know that the problem persists in the latest version and is
not caused by any of your customizations. However, the problem might result from
a small typo or a syntactical error in a configuration file, e.g., `.env`.

Now, before you go through the trouble of creating a bug report that is answered
and closed right away with a link to the relevant documentation section or
another already reported or closed issue or discussion, you can save time for
us and yourself by doing some research:

1.  [Search our documentation] and look for the relevant sections that could
    be related to your problem. If found, make sure that you configured
    everything correctly.[^1]

2.  [Search our issue tracker][issue tracker], as another user might already
    have reported the same problem, and there might even be a known workaround
    or fix for it. Thus, no need to create a new issue.

3.  [Search our discussion board][discussion board] to learn if other users
    are struggling with similar problems and work together with our great
    community towards a solution. Many problems are solved here.

__Keep track of all <u>search terms</u> and <u>relevant links</u>, you'll need
them in the bug report.__[^2]

  [^2]:
    We might be using terminology in our documentation different from yours,
    but mean the same. When you include the search terms and related links
    in your bug report, you help us to adjust and improve the documentation.

---

At this point, when you still haven't found a solution to your problem, we
encourage you to create an issue because it's now very likely that you
stumbled over something we don't know yet. Read the following section to learn
how to create a complete and helpful bug report.

  [Search our documentation]: ?q=

## Issue template

We have created a new issue template to make the bug reporting process as simple
as possible and more efficient for the community and us. It 
consists of the following parts:

- [Title]
- [Context] <small>optional</small>
- [Description]
- [Related links]
- [Steps to reproduce]
- [Checklist]

  [Title]: #title
  [Context]: #context
  [Description]: #description
  [Related links]: #related-links
  [Steps to reproduce]: #steps-to-reproduce
  [Checklist]: #checklist

### Title

A good title is short and descriptive. It should be a one-sentence executive
summary of the issue, so the impact and severity of the bug you want to report
can be inferred from the title.

### Context <small>optional</small> { #context }

Before describing the bug, you can provide additional context for us to
understand what you are trying to achieve. Explain the circumstances
in which you're using P-KISS-SBC, and what you _think_ might be
relevant. Don't write about the bug here.

> __Why this might be helpful__: some errors only manifest in specific settings,
> environments or edge cases, for example, when your documentation contains
> thousands of documents.

### Description

Now, to the bug you want to report. Provide a clear, focused, specific, and
concise summary of the bug you encountered. Explain why you think this is a bug
that should be reported to P-KISS-SBC. Adhere to the following principles:

-__Explain the <u>what</u>, not the <u>how</u>__ – don't explain
    [how to reproduce the bug][Steps to reproduce] here, we're getting there.
    Focus on articulating the problem and its impact as clearly as possible.

-__Keep it short and concise__ – if the bug can be precisely explained in one
    or two sentences, perfect. Don't inflate it – maintainers and future users
    will be grateful for having to read less.

-__One bug at a time__ – if you encounter several unrelated bugs, please
    create separate issues for them. Don't report them in the same issue, as
    this makes attribution difficult.

---

:material-run-fast: __Stretch goal__ – if you found a workaround or a way to fix
the bug, you can help other users temporarily mitigate the problem before
we maintainers can fix the bug in our code base.

> __Why we need this__: in order for us to understand the problem, we
> need a clear description of it and quantify its impact, which is essential
> for triage and prioritization.

### Related links

Of course, prior to reporting a bug, you have read our documentation and
[could not find a working solution][search for solutions]. Please share links
to all sections of our documentation that might be relevant to the bug, as it
helps us gradually improve it.

Additionally, since you have searched our [issue tracker] and [discussion board]
before reporting an issue, and have possibly found several issues or
discussions, include those as well. Every link to an issue or discussion creates
a backlink, guiding us maintainers and other users in the future.

---

:material-run-fast: __Stretch goal__ – if you also include the search terms you
used when [searching for a solution][search for solutions] to your problem, you
make it easier for us maintainers to improve the documentation.

> __Why we need this__: related links help us better understand what you were
> trying to achieve and whether sections of our documentation need to be
> adjusted, extended, or overhauled.

  [search for solutions]: #search-for-solutions


### Steps to reproduce

At this point, you provided us with enough information to understand the bug. 
However, it might not be immediately apparent how we can see
the bug in action.

Next, please list the specific steps we should follow to observe the bug. Keep the steps short and concise, and make sure
not to leave anything out. Use simple language as you would explain it to a
five-year-old, and focus on continuity.

### Checklist

Thanks for following the guide and creating a high-quality and complete bug
report – you are almost done. This section ensures that you have read this guide
and have worked to the best of your knowledge to provide us with everything we 
need to know to help you.

__We'll take it from here.__

## Incomplete issues

Please understand that we reserve the right to close incomplete issues which
do not contain minimal reproductions or do not adhere to the quality standards
and requirements mentioned in this document. Issues can be reopened when the
missing information has been provided.
